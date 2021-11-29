---
layout: post
title: A Catalog of Principles
date: 2021-08-21
---

I often find myself referring to these but sometimes forget the name. Now if
I could only remember I have a list...

## Ockham's razor or Principle of Parsimony

> Entities should not be multiplied beyond necessity
>
> — William of Ockham

Often interpreted to mean "the simplest explanation is likely the right one".

## Conway's Law

> Any organization that designs a system (defined broadly) will produce a
> design whose structure is a copy of the organization's communication structure.
>
> — Melvin E. Conway

## The Rumpelstiltskin Principle

> As the 4,000 year old tale tells, once you have a name for something, you have power over it.

This feel highly related to the fundamental problems of computer science:

> There are only two hard things in Computer Science: cache invalidation and naming things.
>
> — Phil Karlton

The vocabulary we use can restrict our ideas when we have the wrong words and
liberate them when we have the right words.

## Dead Horse Theory

> When you discover that you are riding a dead horse, the best strategy is to
> dismount
>
> — Tribal Wisdom

## Hyrum's Law

> With a sufficient number of users of an API, it does not matter what you
> promise in the contract: all observable behaviors of your system will be
> depended on by somebody.
>
> — [Hyrum Wright](https://www.hyrumslaw.com/)

## Principle of Least Surprise (Astonishment)

> It proposes that a component of a system should behave in a way that most
> users will expect it to behave.

This is usually a good way to vet whether the model you have matches the model
of the user or the model of the world - surprises are often indicative of a
mismatch between these.

## Murphy's Law

> If anything can go wrong, it will.
>
> — Edward Murphy

I interpret this as planning for failure, even if you think it will never
happen.

## Law of Large Numbers

> The average of the results obtained from a large number of trials should be
> close to the expected value and will tend to become closer to the expected
> value as more trials are performed.

One way to think of this is that if you only have a few samples, you should
have no expectation of the samples being close to the expected value. With
many, it is a good bet that they trend to the expected value.

## Law of Medium Numbers

> For medium number systems, we can expect that large fluctuations,
> irregularities, and discrepancy with any theory will occur more or less
> regularly.
>
> — Gerald Weinberg in "An Introduction to General Systems Thinking"

In simple terms, small system are those that you can model analytically
Large systems are those that you can model statistically. Medium systems
neither lend themselves to "small analysis" nor "large analysis". They are
pervasive.

## Single Responsibility Principle

> A class should have only one reason to change
>
> — Robert C. Martin

Often interpreted to mean that any entity (module, class, function) should have
responsibility over exactly one idea.

## Don't Repeat Yourself Principle

> Every piece of knowledge must have a single, unambiguous, authoritative
> representation within a system.
>
> — Andy Hunt and Dave Thomas

Never, ever, copy, code.
