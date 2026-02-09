---
layout: post
title: Cloning Myself (Part 1)
date: 2025-10-06
---

_This post is the part of a series._

Over the last 15 years, I've published about 150 posts. The vast majority of my writing lives behind
various corporate firewalls, but this public collection has become a personal knowledge base. I often
find myself encountering a familiar problem and thinking, "I've seen that before," then digging through
my archive to find a link for someone.

What if I could flip that around? Instead of me searching for the right post, what if a visitor could
just ask a question? The site could then synthesize an answer using my past writing, customized to
their specific query. That’s the goal. My tool of choice: AI.

## The One Fun Constraint

I have one big constraint that makes this project particularly interesting: this website is hosted on
GitHub Pages. It’s been my blog's home for years because GitHub provides the hosting for free (thank
you, GitHub!), and I have no intention of starting to pay for it now.

This means no server-side backend. No API calls to a Python script running on a Lambda. To keep things
free, my entire AI interaction has to run in the browser, borrowing CPU cycles from my visitors. This
implies a hefty initial download and responses that won't be best-in-class. It also implies a lot of fun.

Let's dive in.

## Step 1: Modernizing the Build

To create the custom pipeline this project requires, I first needed to move away from GitHub's legacy 
Jekyll website builder and toward GitHub Actions.

While waiting for lunch, I typed the following into Claude on my phone, typo and all:

> I have a website hosted on GitHib. I want to migrate from the legacy GitHub pages generator
> to a custom generator using GitHub actions. Can you make a pull request to do this migration?

Claude replied that it couldn't create a pull request directly but was happy to generate the content
for one. It just needed a little more information.

> This is using the standard Jekyll setup.
>
> The repository URL is https://github.com/garretfick/garretfick.github.io
>
> It is hosted at a custom domain: garretfick.com

Just like that, while waiting for a sandwich, I had a complete GitHub Action definition and clear
instructions on what to change.

Later that day, I continued the conversation. My next goal was to establish a local development loop
for faster testing.

> I want to be able to run the generation and actions locally,
> just like how GitHub actions might work. This will help with testing. Can you suggest how in might do this?

Claude correctly identified that I'm familiar with `act` and suggested I use it. But it didn't stop
there. It anticipated that my GitHub token wouldn't have the right permissions to push changes from
my local machine and, more importantly, that I probably wouldn't want to deploy every local test build anyway.

Claude provided me with a second, distinct actions file tailored specifically for local development.

If you are astutely paying attention, Claude suggested two different workflow files, having almost the
same content. That sounds like violation of the DRY principal. It took one more prompt:

> Is there some way to not have the duplicated code, perhaps by providing an optional argument. That would
> ensure consistency between my testing and production.

Just like a new developer, sometimes you to remind AI of software development best practices. Nevertheless,
this AI-supported development felt like magic.

## What's Next?

With the build pipeline modernized, the next step is to start tackling the core AI problem: converting all my posts into a format the machine can understand and building the in-browser interface to query it. Stay tuned.