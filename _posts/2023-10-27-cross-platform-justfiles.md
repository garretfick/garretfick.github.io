---
layout: post
title: Cross Platform Justfile
date: 2023-10-27
---

[just](https://github.com/casey/just) is a cross-platform task runner. I use `just` extensively
to define the build tasks for [IronPLC](https://www.ironplc.com).

I use `just` so that my local builds and the continuous integration builds are as close as possible.
`just` makes that work for multiple platforms (IronPLC supports Windows, macOS and Linux) and multiple 
languages (IronPLC uses Rust, TypeScript and Python). It is trivial to install and run on most
platforms.

## Problem

The biggest problem I had was getting `just` to work on Windows. `just` runs each command in a shell
and `sh` is the default for Windows. Getting `sh` to work means running through Git Bash (or similar)
which defeats being trivial to install and run.

I wanted to use `just` as a task runner but making it work having the exact same commands via `sh`
was an enormous headache.

## Insight

The key insight came as I was trying to make integration tests work for Visual Studio Code. For macOS,
these run directly:

```sh
npm run test
```

For Linux, these run inside an Xvfb (X virtual framebuffer) context:

```sh
xvfb-run -a npm run test
```

I thought I needed a way to run the same command on each platform. Instead, I needed a way to make
if feel as though it ran the same command on each platform. Different paths for different platforms
was not duplicating code - that was actually what I needed. The pieces fell into place when
I stopped trying to force `sh` onto Windows.

## Solution

My solution is to use `sh` on macOS and Linux and use PowerShell on Windows. For most cases, those
are exactly the same thing. In cases where they are different, I divide and conquer using `just` functions to divide.

First, I set the default shell for Windows to PowerShell:

```sh
set windows-shell := ["powershell.exe", "-c"]
```

Then, when the commands vary, create hidden commands for each platform, for example:

```sh
test:
  {% raw  %}just _test-{{os()}}{% endraw %}

_test-windows:
  npm run test

_test-macos:
  npm run test

_test-linux:
  xvfb-run -a npm run test
```

I use this strategy when I want to run the same thing on different platforms and when I
want different platforms to do different things that are specific to the platform. For
example, the `package` task on Windows creates a Windows installer and the `package` task
on macOS creates a Homebrew tap.

There are lots more examples in the [IronPLC repository](https://www.github.com/ironplc/ironplc). Especially look that there is more than one `justfile` in the repository.