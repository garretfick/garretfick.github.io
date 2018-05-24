---
layout: post
title: How to static_cast std::unique_ptr
date: 2013-01-01
---

I've been writing a lot of code using `std::unique_ptr`, new in [standard library changes for C++11](http://en.wikipedia.org/wiki/C%2B%2B11#C.2B.2B_standard_library_changes). One of the thing the library doesn't provide is a way to cast `std::unique_ptr`, for example, from a base type to a derived type.

I wrote a couple of helper functions that is probably useful for someone else. They obey the basic rule for `std::unique_ptr`, that one object owns the memory. They also work well with the `auto` keyword, and so can save you a lot of typing

```
template<typename D, typename B>
std::unique_ptr<D> static_cast_ptr(std::unique_ptr<B>& base)
{
    return std::unique_ptr<D>(static_cast<D*>(base.release()));
}
  
template<typename D, typename B>
std::unique_ptr<D> static_cast_ptr(std::unique_ptr<B>&& base)
{
    return std::unique_ptr<D>(static_cast<D*>(base.release()));
}
```

You can see the code in action on [ideone.com](http://ideone.com/waVNu).

*Note* As JQ notes below, this code is not safe to temporarily cast the pointer.