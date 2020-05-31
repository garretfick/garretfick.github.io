---
layout: post
title: Avoiding #include in Headers
date: 2011-10-13
---

Last week I wrote about why I think #include in headers are evil. Sometimes #includes in headers is a result of laziness, but other times, because there is apparently no other alternative. In reality, there is nearly always an alternative.

## Forward Declarations

A common practice is to forward declare classes and structs. This isn't anything new, and the syntax should be pretty familiar to any C++ developer:

```
class MyClass;
struct MyStruct;
```

What is comparatively less common is forward declaring an enum. The syntax follows the same pattern as with classes and structs:

```
enum MyEnum;
```

However, enums are commonly defined within the context of a class

```
class MyClass2
{
    enum MyEnum2 { VALUE1, VALUE2 };
};
```

This works, so long as you don't need to use any of the definitions in the class.

...