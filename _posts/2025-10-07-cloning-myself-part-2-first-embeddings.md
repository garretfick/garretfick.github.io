---
layout: post
title: Cloning Myself - Basic Embeddings (Part 2)
date: 2025-10-07
---

_This post is the part of a series._

With the groundwork from Part 1 laid, it was time to get to the core of the project: generating the embeddings that would 
power my AI clone. My tool of choice? Gemini. I figured since that's where I first asked about building a clone, it would 
have the necessary context. A flawless assumption, right?

## The Embedding Script

I started by asking Gemini to generate the embeddings file.

>  Can you give me specific instructions on how to create the embeddings.json file? I want to be able to test this locally too.

My brilliant plan immediately hit a snag. By switching AIs, I'd lost all the context from my previous session. Gemini produced a Python script, but getting it to play nice with my DevContainer setup was another story. After several failed attempts, I resorted to the classic "break system packages" approach in the Docker container. To make matters worse, Gemini was convinced my website was Python-based, further proof that context is everything.

## Automating the Mess

Wrestling with a local script felt brittle, so I decided to automate the process with a GitHub Action.

> Can I have a GitHub actions generate the embeddings.json file?

This seemed like a more robust path. At this point, you might be wondering—why not just use an AI in my IDE where it has all the context? The short answer: I burned through my free trials for Cursor, Windsurf, and Kiro. How I managed that is a post for another day.

Predictably, the first pass at the workflow failed. It ran at the wrong time, causing the site generation to overwrite my precious embeddings.json file. It was also missing dependencies. While the fixes were straightforward, asking the AI to debug its own broken workflow was surprisingly unhelpful. After some manual tinkering, I finally had a workflow that reliably generated the embeddings on each build.

## Building the Front-End

Now for the fun part: making it all work on a web page. I needed to use transformer.js to take user input and find the most relevant content from the embeddings.

> How do I use transformer.js on my site? For example, can you write the JS code that would be needed to take input from a text area and return a response?

Gemini produced a functional piece of code, but it completely ignored the embeddings.json file we had just worked so hard to create. It took a bit of back-and-forth to get it on the right track.

> I don't see where this loads the embeddings.json file. Is something missing?

And then, more directly:

> Can you write the JS to do this?

With that, I had a web page that… sort of worked.

The clone was alive! But it was slow, clunky, and running entirely in the browser. I asked a
question that I had answered on my website.

![](/static/img/blog/cloning-myself-part-2/what-is-moral-maze.png)

The answer was nonsense. The next step is to figure out how to make it better. To be continued.