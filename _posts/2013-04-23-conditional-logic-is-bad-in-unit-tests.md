---
layout: post
title: Conditional Logic is Bad in Unit Tests
date: 2013-04-23
---

I've follow the mantra that branch points in unit tests are bad practice, but I'd never tried to give specific reasons why it is bad practice. If you think about it, it is actually quite easy to see why. Let's look as a simple example (written using [GoogleTest](https://code.google.com/p/googletest/)).

**Option 1**

```
Object* myPtr = ::GetObject();
ASSERT_TRUE(myPtr != NULL);
EXPECT_EQ("name", myPtr->Name();
```

**Option 2**

```
Object* myPtr = ::GetObject();
if (myPtr != NULL)
{
   EXPECT_EQ("name", myPtr->Name();
}
```

I immediately see three reasons to prefer the first option:

Is simpler to read. No if magic in your head. In this case it is simple, but we have all seen code with multiple branch points that is nearly impossible to follow.

It better expresses the requirements (the pointer must not be `NULL`). In comparison, the code with the branch says the pointer can be `NULL`, but if it isn't, then the `Name` must be `"name"`. It is subtle, but an important distinction.

The if statement introduces a potential error. If you mistakenly typed if (`myPtr == NULL`) then, the `EXPECT_EQ` would not execute, but the test would still pass. Fewer branch points increases your confidence in the test.

The same logic applies to other flow control statements, such as `for`, `while`, etc.