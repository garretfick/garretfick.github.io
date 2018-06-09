---
layout: post
title: To Tuple or Not
date: 2017-05-11
---

Libraries for C++, C# and other language frequently provide tuple objects as an easy way to create n-pairings of items and objects, for example [std::pair](http://en.cppreference.com/w/cpp/utility/pair) and [System.Tuple](http://msdn.microsoft.com/en-us/library/system.tuple%28v=vs.110%29.aspx).

Because they are "cheap to write" it is temping to use them instead of writing a separate class or struct. But, they come with side effects. The names of the members are not very descriptive. For example, in C++, you get first and second and in C# you get Item1 and Item2, etc.

So, when should use these tuple types and when should you write your struct/class? I give the following advice:

> If the struct/class you would write would have member names like file1 and file2, then use a tuple type. This usually happens when the types of the objects are the same.

> Else if the type is used only within a single function, then use a tuple type.

> Otherwise, create your own class/struct.