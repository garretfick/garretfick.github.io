---
layout: post
title: Do a Code Review
date: 2011-10-12
---

I've been working on a major project at work since the beginning of the year. As usual, I can't talk about specifics. Is is my latest major project at work, and the project is finally winding down, which is good because I put in quite a few weekends to keep things on track.

I requested a code review from one of my co-workers last week. I'm in the "no code review required" group at work, so this was completely optional, but I wanted a review for a few reasons. There is a lot of new code and it is good if someone else understand it, I'm also not beyond improving or learning something new, and maybe even find some bugs. It was a review of much of the code I've written over the last 4 months, and took about 1 hour. Was it worthwhile? We found one bug each (both memory leaks), and the reviewer had a good suggestion to convert a new iterator I introduced to derive from the [STL iterator template](http://www.sgi.com/tech/stl/forward_iterator.html). In 1 hours, we found 3 relatively small improvements to the code (two of which I fixed during the code review). It is also unlikely that these issues would ever have been found by black box testing, so I think the code review was highly successful.

This is the second time I've requested a code review, and I think this is something I will continue in the future, even as my experience increases. The opportunity to find and fix problems and improve my code is just too attractive.