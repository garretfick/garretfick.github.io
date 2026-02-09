---
layout: post
title: The Integration Test Partial Workflow
date: 2024-02-05
---

This post is part of a series on the [IronPLC deployment and integration pipelines]({% post_url 2023-11-13-ironplc-pipeline %}).
This topic describes the integration test workflow.

## Strategy

The integration test workflow ensures compatibility between
independent components of IronPLC. As a reminder: IronPLC has three primary
components, of which the following two are relevant from the perspective of
integration testing:

* the Visual Studio Code Extension
* the compiler 

In general, there are multiple versions of each. If the extension has versions

$$\vec{E} = \{E_1, E_2, E_3\}$$

and the compiler has versions

$$\vec{C} = \{C_1, C_2, C_3\}$$

For this simple scenario, there are 9 possible test scenarios. In general, the number
of test scenarios is

$$|\vec{E} \times \vec{C}| = |\vec{E}| \cdot |\vec{C}|$$

Testing each scenario will not scale.

What I needed was a strategy that turns this into a reasonably sized set. It is possible
to reduce this set to something that's manageable. Let's assume that $C_n$ is the last
released compiler version and that we desire to release $C_{n+1}$. Similarly, let's assume that
$E_m$ is the last released extension version and that we desire to release $E_{m+1}$. 

We can reduce the number of combinations if we consistently ensure the following scenarios pass:

$$\{C_n, E_m\}, \{C_{n+1}, E_m\}, \{C_n, E_{m+1}\}, \{C_{n+1}, E_{m+1}\}$$

Mathematically, we are using the transitive property to guaranteed compatibility.

## Implementation

The integration test workflow implements this test strategy. I should be
precise because the workflow doesn't actually implement all parts of the
strategy today, but it does make it possible in the future.

This resulted in a build recipe that takes in version numbers
as the inputs. The test steps do the following:

1. a step that installs Visual Studio Code
1. a step that installs the Visual Studio Code Extension
1. a step that install the compiler
1. a step that opens a file in Visual Studio Code and looks for
   an indication of compatibility (a log statement)

This is very much a smoke test. That is, a single log statement does not indicate
broad compatibility but most of the API is determined by the Language
Server Protocol which limits much of the API surface. Moreover, that smoke test 
was sufficient to detect a real API regression that I introduced but did not
detect while implementing the test. Sometimes simple works well.

As usual, most of the pipeline logic is in a [justfile](https://just.systems/) recipe to enable testing without running the workflow. The step is then:

{% raw %}
```yaml
# Configure the execution environment
- uses: taiki-e/install-action@just

# Execute build recipes
- name: End to end test
run: just endtoend-smoke ${{ inputs.compiler-version }} ${{ inputs.ironplcc-installer-x86_64-windows-filename }} ${{ inputs.extension-version }} ${{ inputs.ironplc-vscode-extension-filename }} ${{ inputs.ironplc-vscode-extension-name }}

```
{% endraw %}

## Rough Edges

First, test scenario description left off two important dimensions - operation system and architecture.
IronPLC supports Windows, macOS and Linux. Further, IronPLC support x86_64 and ARM. Testing those dimensions
adds a lot of complexity.

The easiest scenario was where there is a specific downloadable installer - Windows. Thus, the only scenario
I ended up implementing was Windows.

Second, Visual Studio Code offers a command line to install extensions. After much trial and error, I concluded
the command line is broken. I thus reverse engineered the expected result.

Third, in order to download and install artifacts, I needed to both:

* have the installer install without admin privileges (I migrated from an MSI to NSI stack)
* make the release public as a pre-release

Finally, there is no easy way to know that an extension has successfully started a language server
(i.e. IronPLC compiler). I thus added logging to the IronPLC compiler so that I could detect that it had started
correctly after opening a file:

{% raw %}
```powershell
IF (Test-Path "{{env_var('LOCALAPPDATA')}}\Temp\ironplcc\ironplcc.log" -PathType Leaf) { exit 0 } ELSE { exit 1 }
```
{% endraw %}

Given my "when I'm interested" rate of development, creating the end-to-end integration test was months
of effort.