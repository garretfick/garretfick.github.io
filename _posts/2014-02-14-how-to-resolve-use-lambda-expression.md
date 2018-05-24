---
layout: post
title: How to Resolve Use Lambda Expression
date: 2014-02-14
---

As someone relatively new to C#, I don't always think of the simplest way to express my intent. We use [Resharper](http://ficksworkshop.com/www.jetbrains.com/resharper) in my workplace and it is quite good at picking up where I think too much in C++.

A common message I get is

```
Use lambda expression
```

but I usually forget how to fix it, even though it is trivial. Let's look at a simple example that gives the message:

```
List<int> list = new List<int>();
//The list gets populated with values
List<int> matches = list.FindAll(val => { return val != 9});
```

The fix is simple, remove the braces and return statement

```
List<int> list = new List<int>();
//The list gets populated with values
List<int> matches = list.FindAll(val => val != 9);
```