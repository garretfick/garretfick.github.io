---
layout: post
title: What is Base in Merge
date: 2013-10-18
---

It isn't like I haven't merged before, it's more I never really really thought about it. When you doing a three way merge between branches, you have three files, and you're trying to create a fourth:

* yours: in your branch
* theirs: in the source branch
* result: what you will create
* base: a common base

Because the merge tool picks these for you automatically (actually, it is the source control), I've never really thought about what is base, particularly when the branch history starts to get more complex. If you think about what you need to do, then the answer is relatively straightforward. _The objective of merge is to take a set of changes in one codeline and apply those changes in another codeline._ With that understanding, the meaning of base should be obvious. Base is the last version in the source branch from which the file was merged.

![](https://s3-us-west-2.amazonaws.com/ficksworkshop/media/blog/what-is-base-in-merge/merge.png)