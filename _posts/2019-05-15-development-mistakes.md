---
layout: post
title: Development Mistakes
date: 2019-05-15
---

Learning from Mistakes

Making mistakes is not fun but it turns out that mistakes are often very good learning opportunities. While on vacation,
I got to spend some time thinking about some mistakes I've made. (For interest, the particular prompt was "CRUD only when
you can afford it" which led to a little reminiscing.) As a bit of a change from my normal post topics, I present some
classic software engineering mistakes and what I've learned from them.

## Eating Dog Food When You're a Vegetarian

NIH (not invented here) syndrome is a pretty common problem for software organizations. It's more fun to develop everything
from scratch and there is a sometimes true belief that a better solution is found by focusing only on your particular use case.

At National Instruments, my first major project was to replace our nightly automated regression system. As a company that
also produces software for automated testing, I decided that we should use NI TestStand as the execution engine,
a great product for automating hardware testing. It also turned out our group manager at the time was the former manager of
NI TestStand.

Things initially went well. I was able to get something up and running pretty quickly.
In addition the execution engine itself (which processed tests described in XML), there was a multi-agent execution manager and
monitor, a backend for storing results, and a web front end for viewing/interacting with results. This all connected with the
build system or could be run locally. Reasonably complex and with how little I knew at the time, it's amazing it worked.

It did work and we eventually transitioned to it but I don't think it ever worked well. The reasons are complex, but a significant
reason was using the wrong tool for the job. Using an existing test framework - great idea. Using an existing test framework not
typically used for software testing that had complex shared dependencies with the software under test, was missing important
capabilities that needed to be written from scratch - bad idea.

When the project was starting, I had looked for other frameworks and even found other open source frameworks that were far more purpose
built, but I shelved those thinking that I should be supporting (my naïve view of) NI's broader vision. I believe our use case didn't
fit with TestStand vision at the time. NI didn't reap benefits from eating our own dog food and having to extend the system in many
ways consumed valuable development capacity. Twice the loss!

**Lesson** It's important to support organization objectives, but you can only do that if there is either a good fit or high-level support for
making it a good fit. Absent those, you might as well be feeding a diet of meat to an herbivore.

## The Overly Ambitious Refactor

Fast forward a number of years, I found myself having extra time in our project plan having completed my features early. (This is when
waterfall was still in vogue). Another developer had been on a complex and risky architecture project aiming to split the application
into two processes - one for the simulator and one for the user interface. They would be able to exchange data through some API.

```
-------------    ------------------
| simulator |<-->| user interface |
-------------    ------------------
```

I took a look at the project and concluded that half the work was wasted effort because automated test results were meaningless.
The actual structure looked more like the following:

```
-----------------------       -------------------
|           | XML     | <-->  | automated tests |
|           -----------       -------------------
| simulator           |
|           -----------       -------------------
|           | binary  | <-->  | user interface  |
-----------------------       -------------------
```

The simulator provided two interfaces - one based encoded as XML and another encoded in binary. The belief in correctness was based
on the XML encoding, but that shared almost nothing with the binary serialization. Which data members were serialized and how was
entirely different.

Being sufficiently ambitious, I embarked on a plan to developing a common API that could serialize in binary for performance or XML
for tests. (Had this been at another company, we might have called this protocol buffers.) And on I went trying to rip out the old code
and insert my new code. Given the scope of the API, I had a lot of work ahead of me and while that was going on, the primary developer
was continuing to add capabilities.

In the end, the scope was too big for me to consume and I couldn't get all of it working. I was simply too ambitious, trying to take on
the whole thing at once. Instead, I should have taken a far less ambitious approach where I figure out a way to make a small change,
validate that the functionality was unchanged, then move on.

**Lesson** When refactoring, make the smallest possible change. Then repeat.

## Needing Some Alone Time With Your Project

Fast forward a few years, I was working at ChinaNetCloud where I had been hired to develop a new web portal for managing operations as a
service (OaaS). The portal was to be written in PHP using Laravel - a framework and language both new to me. Not only that, but I had
joined the company perhaps 3 weeks prior, so I was still getting familar with the business.

Perhaps becauase I was new, I agreed that I would get a week to learn the framework, and the we would throw a team of about 5 developers
at it. We set a goal of reimplementing a  help-desk ticket system in 2 weeks. It involved carefully dividing up the work, which we
did successfully. And in 2 weeks, we had replicated the functionality we had planned in a mess of code.

In the race to implement, few decisions about the architecture had been made. Coding standards were not established. We didn't have
agreement on whether on not to use the ORM. We didn't have tests. We didn't make effective use of the framework. In that two weeks,
we generated enough technical debt that two years later, it was still not all paid back.

Instead, we needed an expert in Laravel to show us the way. That could have been me if I'd demanded more time to learn, and iterate.
That could have been a consultant to review code or develop the first system. Whatever it was, we needed a good starting spot.

**Lesson** When you are investigating something new, it takes time to get oriented, and you need that before throwing more resources at it.

## Have I Learned?

That's 3 big lessons I've learned along the way. While they were learned the "hard way", none of them were catastrophic. Most importantly,
I've had the opportunity to make similar decisions, but have not repeated those mistakes, but that makes for a far less interesting post.
