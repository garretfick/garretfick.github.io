---
layout: post
title: #include is Evil
date: 2011-10-05
---

Any seasoned C/C++ developer should already know that `#include` in header files are evil. Not quite as [evil as goto](http://xkcd.com/292/) (see below), but close. There are any number of reasons that `#include` in headers evil, from creating [spaghetti code](http://en.wikipedia.org/wiki/Spaghetti_code) and increased dependencies to [reducing compile times](http://developers.sun.com/solaris/articles/CC_perf/content.html).

[![1](http://imgs.xkcd.com/comics/goto.png)](http://xkcd.com/292/)

I think the most important reason is developer productivity. Adding a `#include` in a header is a seemingly inexpensive thing to do. Indeed the immediate cost is the same as a forward declare and less than some other techniques, so it might seem that from a productivity perspective, they are great. In reality, the true cost of these insidious fellows comes later.

A large project with thousands or tens of thousands of files takes a significant amount of time to compile, hours for very large projects. In terms of developer time, it is expensive to compile from scratch or even a significant portion of the project. And that is where #include in headers shine - each nested header increases the probability that you will need to recompile a significant portion of your project. The small decision to use a #include rather than a forward declare may cost hours or days of developer time wasted recompiling unrelated code because some nested header changed.

If you want to avoid them all costs, why are they such a common problem? Partly because of laziness, but also because developer often don't know how to avoid them. Next time we'll see some practical solutions to reducing nested headers.