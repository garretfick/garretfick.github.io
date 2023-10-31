---
layout: post
title: Justfile "Targets"
date: 2023-10-27
---

[just](https://github.com/casey/just) is a cross-platform task runner. I use `just` extensively
to define the build tasks for [IronPLC](https://www.ironplc.com), in part so that local builds
and the continuous integration builds are as close as possible.

`just` runs tasks and has no opinion when it comes to what the tasks are.

## Problem

IronPLC is contained in a single repository that includes the compiler in Rust, the Visual Studio Code
integration in TypeScript, the website in reStructuredText (Python), and build task definitions.
In fact, some website pages take content directly from the compiler. Keeping things in one repository
simplifies the build and test process.

IronPLC builds using GitHub Actions. It is possible to create complex actions, but it is usually better
to put any complexity into tasks (scripts) so that they can be run outside of the automated build. 

This is the crux of the problem: what are the tasks?

It is possible to define tasks based on each component's tasks, such as Cargo, NPM or Maven, but those
tasks are not inclusive. The Cargo build tasks don't create the Windows installer. Each component
defines tasks slightly differently.

## Insight

What I needed was a simple vocabulary of tasks that integrations well into with the automated build
and is simple enough to not obscure each component's build system.

## Solution

I ended up with just a handful of regular build tasks.

* `version` - updates the version number
* `setup` - installs dependencies
* `build-and-test` - builds and tests for release
* `package` - creates the distributable artifact
* `publish` - publishes distributable artifact
* `endtoend-smoke-test` 

The one that I had the most difficulty was `build-and-test` and ended up calling it exactly what it does.