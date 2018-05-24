---
layout: post
title: Avoid Loading of Unnecessary Symbols
date: 2012-03-09
---

Setting up Visual Studio to use a symbol server can greatly improve your ability to debug problems. However, adding a symbol server can significantly slow down debugging as Visual Studio searchs for symbols not in the cache each time a DLL loads for a debugging session and loads symbols for DLLs that are not relevant for your debugging. You'll get a huge speed-up by telling Visual Studio to skip loading symbols for these modules. Follow the steps below tell Visual Studio to skip loading these symbols.

## Identify Modules to Skip


1. Start debugging
2. In the Output window, search for "Cannot find or open the PDB file"

## Exclude Modules from Automatic Symbol Loading

1. Click `Tools > Options...` and select the page `Debugging > Symbols
2.  Click `Specify excluded modules`
3.  Add each of the items from the previous step to this list

## Add Extras

This will capture a good number of symbols to skip loading, but you can skip more. In particular, showing the Windows Open/Save dialogs loads a number of modules, and I've set Visual Studio to skip these too (even through it can find symbols for many) because these modules are used only with the context of the Open/Save dialogs, and are not relevant for a normal debugging session.