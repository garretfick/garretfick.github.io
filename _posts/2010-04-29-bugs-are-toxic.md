---
layout: post
title: Bugs are Toxic
date: 2010-04-29
---

I frequently think about quality and in my job that means bugs. Severity, visibility - simply bugs. I've mentioned before that I don't buy the prevailing wisdom that we can't fix everything.

Today I spent some time fixing a bug that will never happen in practice - it was in code I wrote only for internal testing. The bug could not occur outside of this case so I did not have to fix it. But it later occurred to me that the quality of the code I write today affects the quality myself and others develop in the future. Bugs today invite more in the future.

Why is this?

When developing new features, I believe one objective is to develop at a quality level that matches of exceeds the surrounding code. This view may not be explicit; it can be implicit for example when talking about limitations and how well rare cases need to be handled. If the surrounding code is buggy there may be a view that other bugs will cause problems before this new case is hit and so there is no point in doing something elegant. In this way a new bug is introduced. I find idea troublesome because it suggests once software has a bug it is nearly impossible to go to a no bug state. Or equivalently, it is nearly impossible for software to improve in quality.

The question is then what do I do? While I still brewing on the idea, I think the solution is to be aware and not restrict yourself to anything but the highest quality although that sounds like a copout to me. Any better ideas?