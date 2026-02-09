---
layout: post
title: The Version Partial Workflow
date: 2023-11-19
---

This post is part of a series on the [IronPLC deployment and integration pipelines]({% post_url 2023-11-13-ironplc-pipeline %}).
This topic describes the version partial workflow.

## Strategy

The version partial workflow increments the version number so that each release
has a unique number. There are a couple common approaches:

* [semantic versioning](https://semver.org/)
* [calendar versioning](https://calver.org/)
* incremental versioning

In reality, the semantic versioning strategy is the only one that supports
compatibility between releases without maintaining a list. I chose semantic
versioning because I expect developers will use different versions of the IronPLC
components.

Semantic versions have 3 parts: `MAJOR`, `MINOR`, and `PATCH`. To keep things
"simple", I decided to ignore the `PATCH` component, incrementing either `MAJOR`
or `MINOR` on each new build. Although it is possible to do this automatically
with various tools and labeling of commits, I instead opted to thoroughly test
for backwards compatibility and then manually increment `MAJOR` as needed.

## Implementation

The version partial workflow updates the version number to the next number in the
sequence. Generally, I try to put all the pipeline logic into [justfile](https://just.systems/)
recipes so that I can test locally. That resulted in a build recipe with three steps:

1. a step that determines the next version number by looking at the tags in the repository
2. a step that updates the version number in each component and commits the change
3. a step that commits the update to the repository

The separate step to determine the version number ensures that unexpected output cannot
accidentally affect the version number (for example if updating a component manages to write
to standard output). It also reserves the possibility of specifying a version number instead
of automatically determining the version number.

The separate setup to commit the update helps reduce the risk of locally changing the author
name and email (as far as I know, you cannot specify the author via the command line when
creating a tag).

{% raw %}
```yaml
# Execute build recipe
- name: Get the next version number
  id: nextversion
  run: echo "version=$(just get-next-version minor)" >> $GITHUB_OUTPUT
- name: Update version number in the repository
  run: just version ${{ steps.nextversion.outputs.version }}
- name: Commit version number to repository
  run: just commit-version "Continuous Integration" "garretfick@users.noreply.github.com" ${{ steps.nextversion.outputs.version }} 
```
{% endraw %}

The partial workflow thus produces three outputs that are variations of the version number.

{% raw %}
```yaml
outputs:
    # The tag that is the Github release
    gh-release-tag: ${{ format('v{0}', steps.nextversion.outputs.version) }}
    # The tag in the git repository (e.g. v1.0.0)
    commit-tag: ${{ format('v{0}', steps.nextversion.outputs.version) }}
    # The version number of components (e.g. 1.0.0)
    version: ${{ steps.nextversion.outputs.version || '0.0.0' }}
```
{% endraw %}

## Rough Edges

All of the above works reliably. However, there were some important rough edges. Developing and testing is difficult. Failed runs still increment the version number resulting in valid but unused version numbers. There is a `dryrun` flag
that does as much of the build as possible, omitting any item that commits or publishes a change.

To make that work, the version workflow only sets outputs when not in `dryrun` mode.

{% raw %}
```yaml
outputs:
    # The tag that is the Github release
    gh-release-tag: ${{ !inputs.dryrun && format('v{0}', steps.nextversion.outputs.version) || '' }}
    # The tag in the git repository (e.g. v1.0.0)
    commit-tag: ${{ !inputs.dryrun && format('v{0}', steps.nextversion.outputs.version) || '' }}
    # The version number of components (e.g. 1.0.0)
    version: ${{ steps.nextversion.outputs.version || '0.0.0' }}
```
{% endraw %}

Lastly, the version workflow creates the GitHub Release.
I have mixed feelings about having the version step create the GitHub Release. It is possible to defer
creating the GitHub Release until after creating all build artifacts, but later steps would need to know
about the names of all build artifacts. I decided to create the GitHub Release because GitHub Actions
have limited abilities to pass information between workflows and steps.