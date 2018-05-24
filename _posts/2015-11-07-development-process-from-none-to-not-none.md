---
layout: post
title: Development Process - From None to Not None
date: 2015-11-07
---

A pretty common question I'm asked is what kind of R&D process we used (and I implemented) at my last company. The question is enormous because it covers at least tracking bugs, handling feature requests, code branching strategy, testing and deployment.

The answer is even more difficult to answer because our process evolved as we got better and responded to what was happening around us. I think the evolution is instructive because it represents real choices we faced.

If this is a story, then it has to have a beginning. The story for me begins with the state of affairs when I joined. The initial process was something like the “anti-process”.

## Bugs and Features

Bugs and features were tracked in Trello. Since you probably don’t know Trello, let me introduce Trello.

> Trello is a collaboration tool that organizes your projects into boards. In one glance, Trello tells you what's being worked on, who's working on what, and where something is in a process. ([Trello](http://help.trello.com/article/708-what-is-trello))

It isn't a tool specifically for software projects. It is really more like a organized to-do lists.

Our projects were organized into feature-specific boards typically with the states “Ideas”, “To Do”, “Assigned”, “Doing”, and “Done”. Although they existed, the data was often obsolete, and a lot of changes were made without going through the boards.

If that still isn't clear, you can see an [example on Trello](https://trello.com/processinitialstate).

## Testing and Deployment

From a product perspective, the product was running on a combination of Heroku (using their amazing automated build and deployment mechanism) and Amazon S3 (for static file hosting).

Question #1: how did we keep those systems in sync? Manually. That great automated process, um, next question.

Question #2: how did we test things before deploying on the production server? We didn’t and couldn’t because most things were hard coded. In fact, if you wanted to test locally, you still needed to connect to S3 because many of the CSS/JS you needed only existed on S3.

But of course we could run the unit tests, right? Hint - for us, it was really easy to calculate code coverage. Still stumped? 0%. Yep. No tests.

Question #3: how did we share code? By deploying to the production server or by email. Yes, you read correctly.

Question #4: how did we know if anything was crashing? Hopefully we would visit the page or maybe a site visitor would email us. And if it only crashed on the production server, how would we diagnose the problem? By deploying brand new code to turn on debug, and then redeploying code to turn it back off.

## A Way Forward?

There is of course more, but I’m still traumatized and you probably already get the idea.

If this sounds like your organization, then I have great news for you. We got better and over the next few posts, I’ll tell you step-by-step how we did it.