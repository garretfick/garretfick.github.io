---
layout: post
title: How I Review Code
date: 2014-04-30
---

For the group I work in at National Instruments, every piece of code we commit is reviewed by at least someone else. I've wrote before about why I think code reviews are important. Since I do many (or most) of the reviews, I think it is really useful for my colleagues to know how I do the review, and what I care most about.

I'll describe my overall process, the types of comments I tend to give, and share some tips for making the code review easier. This isn't a complete list, but should give you an overall idea of how I work and what I care most about.

## My Review Process

### Pass 1 - Details

Generally, I'm most interested in the overall structure, but it's hard to get that picture when I don't know what changed. Usually, I'll go through the code and look at everything that changed.  This is where I notice things like function names, syntax. Can you write the code a little differently that is easier to read? Can you make things private? Generally anything small and isolated.

### Pass 2 - Overall Structure

The first pass helps me understand all the little pieces that changed. But I understand them independently. After that, I'm interested in the big picture. (This is the part I care most about.)

* Do the changes make sense as a whole? Usually a code review will say what the change does, (plus some other things that the developer noticed). Does the change solve the problem it is intended to solve?
* How does the change fit into the existing architecture? For example, if it introduces a new error handing system, I'll be asking is there an existing system it should be using?
* Are there performance impacts? Are there ways to write the algorithm differently that will perform better? A key place that tends to get my attention is a loop within in a loop, but that isn't the only place. If it is testing code, is the code using VIShellTest when it really only needs HostTest?
* Are there tests for the code that changes? Are they small and independent?
* Is there duplicated code that can be eliminated? Enough said.

It is pretty common in this second pass that I delete comments I made initially. I do my best to understand the code, but as we all know, it is often easier to see how the code works by running it. Since I don't run every piece of code, I sometimes make mistakes in my understanding. Just tell me I'm wrong and I'll learn.

## Types of Comments

I try to give three types of comments: "change to A", "questions", and "general comments". I've been trying to figure how to differentiate between these, and I think I still improve significantly.

I'm also sometimes wrong or unsure, but I think it is better to be wrong than ignore a real issue. Where I'm wrong, please tell me so!

### Change to A

You can identify these because I use very direct language. Usually I think something can be improved (or is even a bug). Usually the change is pretty clear.

### Questions

You can identify these because the comment has a question (and usually a "?"). In these, I'm asking a question. You might the right, or I might be right. It probably makes sense to discuss these in person. Since you submitted the review, it is usually your responsibility to start the discussion. But, I'm always happy to have it.

### General Comments

These are probably the hardest to identify. Sometimes the are written in future tense. "You will need to change this in the future." I don't expect these to be fixed in the review, but of course you can. These are my prediction of the future and it is a suggestion that you might want to change now, in the next change you submit, or sometime in the future.

### Positive Comments

There 's one more type that is my favourite comment type to give. If I really like something, I'll tell you.

## Misc Tips

* I like when the code describes what it does, and what it doesn't do. Most changes are incomplete and expect that there will be more changes in the future. The easiest way to get me to not comment on a piece of code is to say "TODO" and describe what needs to be done. This can apply to almost anything (except perhaps writing tests).
* If there is more than one round of code review, try really really hard to not add more to the code review unless it is related to the comments. You may get more "big change comments" about the new part you added resulting in another round of review. I've written before about the process that I use to avoid this: Shelve-Review-Unshelve
* Before you submit a review, go through every file in the change set and look at the diff. Often when I'm preparing to submit a review request, I'll do this more than once if I make changes. Letting people see the code is like saying "this is my best work." When I submit a review, I want to make sure it really is my best work. My goal is that when I submit a TFS review, the only comment I get is "looks good."
* A TFS code review should be a final check of work. It isn't the best way to check if the architecture is right. Before you submit a review, consider asking someone to look at the architectural changes you are making. Architectural changes tend to cause the most amount of work in code reviews and can cause multiple rounds of review. Having offline discussion can save a lot of effort! (You can ask me any time.)
* I care about automated testing. A lot. I think you should to. You won't get very far without writing good automated tests. I can give a lot of advice on how to write automated unit tests.