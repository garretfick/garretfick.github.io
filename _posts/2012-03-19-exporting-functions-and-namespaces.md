---
layout: post
title: Exporting Functions and Namespaces
date: 2012-03-19
---

Turns out my initial analysis was incomplete. See the end of of the post for details.

## Initial Analysis

Last week, I ran into an interesting issue that I think is a bug in the Microsoft VisualC++ compiler relating to exporting functions and namespaces. The symptom I has was I marked a function for export, using `__declspec(dllexport)`, but then couldn't import the function, giving linker error LNK2019: unresolved external symbol.

After making sure it wasn't a problem with some macros, I fired up [Dependency Walker](http://www.dependencywalker.com/), and sure enough, the function wasn't being exported. It seems that the Microsoft VisualC++ compiler (2010) won't export a function in a namespace if the function name is not fully qualified in the C++ file. This is really easy to demonstrate with a simple example.

Let's assume you want to export two functions, `MyFunc1` and `MyFunc2`, and so your header file contains

```cpp
#pragma once<br>
namespace MyNamespace {<br>
__declspec(dllexport) void MyFunc1();<br>
__declspec(dllexport) void MyFunc2();<br>
}
```

The only difference between `MyFunc1` and `MyFunc2` is how they are implemented in the C++ file

```cpp
#include "Functions.h"<br>
using namespace MyNamespace;<br>
void MyFunc1() {}<br>
void MyNamespace::MyFunc2() {}
```

One of these gets a fully qualified namespace, the other does not. Only `MyFunc2`, with the fully qualified name will be exported, whereas `MyFunc1` will be silently forgotten about.

## Actual Cause

Without the namespace in front of the function, the function is declared in the global namespace. Nothing new or unusual here. So the function is not exported because it can't be found, and the linker doesn't give any error or warning for this condition because the function isn't used internally.