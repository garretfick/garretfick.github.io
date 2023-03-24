---
layout: post
title: Requirements before Design?
date: 2023-03-24
---

The usual definition for engineering is the application of science and mathematics
to solve problems. Implicit in that definition is that problems inherently have
trade-offs. Let's make it explicit:

> engineering is the application of science and mathematics to solve problems
> that have trade-offs

A problem leads to requirements and that leads to a design (that hopefully solves
the problem). For an ambiguous problem, do requirements come before design? Even
if we have a waterfall-based approach (as opposed to agile), how do we approach
finding a solution?

Requirements for **hard problems** are not independent of the design, resulting
in a cycle. This all comes down to what I call the architect's responsibility:

> the architect must ... always be prepared to suggest a way of implementing anything he specifies ...
>
> Brooks, F.P. Jr, The Mythical Man-Month, p55-56

That's just another way of saying:

> ... one can not specify a practically attainable tolerance range out of thin
> air; one must recognize what is possible under commercial conditions of
> production
>
> Shewhart, W.A., Statistical Method from the Viewpoint of Quality Control, p47

Or as I've suggested before:

> It's easy to write a requirement that say "the machine shall takes in 1 J
> and produce 10 J of work". Good luck with the design that going to
> violate the First Law of Thermodynamics.

Requirements for hard problems have an awareness of the design, and that results
in the cycle.
