---
layout: post
title: StyleCop Example Custom Rule Project
date: 2013-11-13
---

A project I'm working on uses StyleCop to automatically enforce a set of style and consistency rules. It took some time for me to get a project setup because the StyleCop SDK is missing a few details. Until I got this right, my rules were never loaded, even if the DLL itself was loaded.

* The namespace is important. It must match the project name.
* You must use .NET Framework 3.5

If you have those setup, then the rest of the guide works correctly.

I also put together [an example project](https://bitbucket.org/garretfick/stylecopcustomrule/overview) that has everything setup correctly in case someone wants to start with that. To use the project

* open the project,
* compile,
* put the output DLL in the StyleCop installation directory
* 
Loading the rules should show the custom rule.

![](https://s3-us-west-2.amazonaws.com/ficksworkshop/media/blog/template-stylecop-custom-rule-project/style_cop_custom_rule.png)

*Note* This project works with StyleCop 4.7. To use with a different version, you will need to update the Reference to point to the right version.