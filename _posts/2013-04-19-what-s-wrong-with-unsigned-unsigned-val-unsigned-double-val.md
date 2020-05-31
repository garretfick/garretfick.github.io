---
layout: post
title: What's Wrong With unsigned unsigned_val = (unsigned) double_val?
date: 2013-04-19
---

During a code review, I was asked why I wrote the following C code:

```cpp
double dval = ...;
uint16_t uval = (uint16_t) MAX(0, MIN(dval, UINT16_MAX));
```

If I am going to store the value unsigned, why do I need the `MAX`/`MIN` values? Won't the cast operator take care of this for us? I'll give you a hint - assume you can't trust the double. Still stumped?

The cast operators are inherently unsafe if the input is out of bounds of what can be stored in the destination. They can do more than just clip the value at the maximum.

```cpp
double dval = 1000000000000;
int ival = (int)dval;
unsigned int uval = (unsigned int)(int)dval;
unsigned int uval2 = (unsigned int)dval;
```

What do you think `ival`, `uval`, and `uval2` will be (on a Microsoft compiler)? The answer may surprise you.

```cpp
ival = -2147483648
uval = 2147483648
uval2 = 3567587328
```

We ended up with a negative value for the integer, a positive value for the first unsigned value, and a random positive value for the second unsigned integer. None of the values makes any sense. If you are casting between types and you don't know if the value is in range, then you must first bound the input with `MIN`/`MAX` or `std::min`/`std::max`.