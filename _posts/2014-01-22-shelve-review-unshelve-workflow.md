---
layout: post
title: Shelve-Review-Unshelve Workflow
date: 2014-01-22
---

At National Instruments, we review every piece of code (or at least for the project I work in). Nothing gets checked in without a second (or more) set of eyes looking at the code. One of the developers I work with has been trying to submit some code for quite a while - unsuccessfully. So what happened and how did I recommend he change his workflow so that he will be able to submit the code.

The first code review took a couple days because it generated a lot of discussion and comments. During that time the developer continued to develop and write new code, using what was being review. When the discussion finally ended, we had yet another code review. This included:

* the original code review
* all the additional changes

Can you predict what happened next? The additional changes generated lots of discussion, and so the code still couldn't be submitted. It is easy to see how this can lead to code that can never be checked in.

In order to submit, the developer should only be reviewing the original code review plus the required changes to that code. All the additional changes should be grouped and treated separately. In this past, this was hard, but since many source control solutions have adopted shelving (or stashing), there is a really easy workflow to keep your changes small and independent.

![](https://s3-us-west-2.amazonaws.com/ficksworkshop/media/blog/shelve-review-unshelve-workflow/shelve_review_workflow.png)

With this workflow, you keep your changes small and independent.