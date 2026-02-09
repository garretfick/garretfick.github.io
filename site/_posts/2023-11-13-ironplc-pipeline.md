---
layout: post
title: Continuous Deployment for a Visual Studio Code Extension with Language Server Protocol
date: 2023-11-13
---

Continuous deployment is the automated delivery of software into production environments.
Continuous deployment goes one (big) step beyond continuous delivery because there are not
manual approval steps. But continuous deployment requires a lot of work, especially for 
reasonably complex set of software applications like IronPLC. This post and ones that follow
describe how I build a continuous deployment pipeline for IronPLC.

There are 3 main components to IronPLC, all written in different languages and having
unique distribution mechanisms. It is supported in Windows, macOS and Linux (including
x86_64 and ARM variants).

| Component | Language | Publish |
|-----------|----------|---------|
| Visual Studio Code Extension | TypeScript | Visual Studio Code Marketplace and GitHub Release |
| Compiler | Rust | Windows Installer,  Homebrew Formula, and GitHub Release |
| Website | Python and reStructuredText | GitHub Pages |

That's quite a few pieces and as the sole developer, I won't have time (or interest) in manually 
releasing. As the same time, I expect the software I own to work. To solve this, I decided I
needed continuous integration
and continuous deployment pipelines.

> In the context of the IronPLC deployment strategy, facing onerous manual testing effort we decided for
> automation to achieve deployment at a predictable cadence, accepting the development effort to build
> continuous integration and continuous deployment pipelines.

## Goals

I want to start with some goals that helped guide the strategy. I've called these goals rather
than requirements because they were best effort.

**The pipeline MUST be 100% automated requiring zero manual steps**

This is the goal. Enough said!

**The pipeline MUST fail if a release is not backwards compatible**

Developers will inevitably install different versions of the IronPLC Visual Studio Code Extension and the Language
Server Provider. Poor compatibility would cause a poor experience.

Also, at some point, there will be a change that breaks backwards compatibility. The pipeline should
block on a change that breaks compatibility to ensure a good experience.

**The pipeline MUST test the same artifacts and distribution channels that developers would use**

It isn't enough to just build and publish artifacts. You have test with artifacts in the same way
your developers would test.

This is pretty difficult to achieve, and I didn't satisfy this entirely. I did however get close.

**The pipeline MUST create version numbers compatible with semantic versioning**

[Semantic versioning](https://semver.org/) is sufficiently common that many developers will understand
the versions by default. Furthermore, many tools expect semantic versioning and this choice prevents
a bunch of other issues.

**The pipeline MUST release for all platforms**

There is no way that I'm going to repeat steps for each
environment.

**The pipeline steps SHOULD be runnable**

It is possible to create complex sets of steps, but that results in very hard to test pipelines.
As much as possible, I want to work to happen in scripts that are runnable on their own.

**The repository release branch SHOULD maintained in a release quality state**

There is no point in having a continuous delivery pipeline if the source isn't release quality.

**There SHOULD be only one repository for all software (except 3rd party components)**

While it is possible to have multiple repositories, it is convenient to have a single repository
because one repository prevents one repository from falling behind another. You feel "bad" releasing
a change that requires a documentation update but you don't update the documentation.

## The Deployment Workflow

The deployment workflow automates building, testing and publishing every week.
To do this, I needed a set of discrete and ordered steps that satisfies the deployment goals.
I eventually settled on a 7-step workflow. Yes, it takes 7 steps.

1. Create a new version number.

   This has to happen early on because build tools ultimately depend
   on the version number of the components. This process automatically updates
   the version number in the code and tags the commit.
2. Build and test in isolation the IronPLC Visual Studio Code Extension.
3. Build and test in isolation the IronPLC Compiler (Language Server Protocol)
4. Build and test the website.

   The website is coupled with the version number and application error
   codes. It is this reason that publishing the website is tied to releases.
5. Create a public accessible pre-release of build artifacts.

   This has to be a "real" release so that the next step will use real artifacts
   with real downloads.
6. Run integration test including backwards compatibility using pre-release build artifacts.
7. Publish build artifacts.

This workflow is defined in `deployment.yaml`.

## The Integration Workflow

The integration workflow automates ensuring that the main branch can be released at any time.
This one is similar to the deployment workflow but skips the publication parts, so it needs
only 3 steps.

1. Build and test in isolation the IronPLC Visual Studio Code Extension.
2. Build and test in isolation the IronPLC Compiler (Language Server Protocol)
3. Build and test the website.

Although it is possible to do integration testing in the integration pipeline, I have thus
far not put in the effort.

This workflow is defined in `integration.yaml`.

## Shared Partial Workflows

The deployment and integration workflows share a lot. I think it is possible to use a single
workflow by adding `if` conditions throughout. I also think conditionals such as `if`
are a smell of poor abstraction so I prefer to avoid `if` conditions where possible.

I borrowed the concept of partials for rendering web pages to avoid duplication and get rid of
the `if` conditions. Each partial is a "function" that implements each significant step.
These partials take in inputs and provide outputs, being a very useful concept.

<img width="300px" src="/static/img/blog/ironplc-pipeline/workflows.png"/>

Each partial workflow has roughly the same structure:

1. Checkout the repository/fetch input artifacts
2. Configure the execution environment
3. Execute build recipe
4. Save output artifacts

For example, the partial workflow for the compiler checks out the repository, installs required build tools, creates the installer, then stores the installer artifact. The `if` condition is how I choose either a particular tag (for the deployment workflow) or HEAD (for the integration workflow).

<img width="600px" src="/static/img/blog/ironplc-pipeline/workflow-steps.png"/>

## Partial Workflow Details

Posts that follow describe in detail the partial workflows.

1. [The Version Partial Workflow]({% post_url 2023-11-19-version-workflow %})
1. [The Integration Test Partial Workflow]({% post_url 2024-02-05-integration-test-workflow %})