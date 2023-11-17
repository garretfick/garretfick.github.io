layout: post
title: The Version Partial Workflow
date: 2023-11-18
---


## The Version Partial Workflow

The version partial determines the next minor version number in the sequence and updates
the code to change all references to the version number. The change is committed to the
repository so that the build is is possible to reproduce the build and so that later 
partials can checkout the tag.

The tags in the repository all start with a `v` prefix. 
That enabled me to use two GitHub Actions to determine the next version number.

{% raw %}
```yaml
- name: Get Previous Tag (the last release)
  id: previoustag
  uses: "WyriHaximus/github-action-get-previous-tag@v1"


- name: Determine next release version
  id: nexttag
  uses: "WyriHaximus/github-action-next-semvers@v1"
  with:
    version: ${{ steps.previoustag.outputs.tag }}
```
{% endraw %}