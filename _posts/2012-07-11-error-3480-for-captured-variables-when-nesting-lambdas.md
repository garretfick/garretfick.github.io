---
layout: post
title: Error 3480 for Captured Variables when Nesting Lambdas
date: 2012-07-11
---

Sometimes you need to nest C++ lambdas, for example if you have an outer and inner for loops and you want to use std::for_each to show that you intend to iterate over every item. Simplified, this looks like

```
#include <algorithm>
#include <vector>

int captured_val;
std::vector<int> v1;
std::for_each(std::begin(v1), std::end(v1), [captured_val](int val1)
{
   std::vector<int> v2;
   std::for_each(std::begin(v2), std::end(v2), [captured_val](int val2)
   {
   });
});
```

In Visual Studio 2010 (and possibly others), nesting lambdas like this gives a compiler error due to the captured variable

```
error C3480: 'mynamespace::`anonymous-namespace'::<lambda2>::captured_val': a lambda capture variable must be from an enclosing function scope
```

Microsoft seems to have indicated this is a [bug that won't be fixed](http://connect.microsoft.com/VisualStudio/feedback/details/560907/capturing-variables-in-nested-lambdas), so how you get your code to compile? You have two options:

1. "Re-capture" into a local variable
2. Capture by reference

## Re-capture

Re-capturing means declaring a variable local to the outer lambda, assigning the captured value. Then use the local variable for the inner lambda.

```
#include <algorithm>
#include <vector>

int captured_val;
std::vector<int> v1;
std::for_each(std::begin(v1), std::end(v1), [captured_val](int val1)
{
   int captured_val_nested = captured_val;
   std::vector<int> v2;
   std::for_each(std::begin(v2), std::end(v2), [captured_val_nested](int val2)
   {
   });
});
```

## Pass by Reference

If that doesn't work for you, you can pass the value by reference, and everything works as you would expect.

```
#include <algorithm>
#include <vector>
 
int captured_val;
std::vector<int> v1;
std::for_each(std::begin(v1), std::end(v1), [&captured_val](int val1)
{
   std::vector<int> v2;
   std::for_each(std::begin(v2), std::end(v2), [&captured_val](int val2)
   {
   });
});
```

An enterprising individual might look at the assembly for each to see which is more efficient, but I'm waiting until I see it have any performance impact.