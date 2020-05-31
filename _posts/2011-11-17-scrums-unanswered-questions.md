---
layout: post
title: Scrum's Unanswered Questions
date: 2011-11-17
---

Lately, I've been doing a lot of reading on Agile, and specifically on Scrum. Admittedly, when I started reading, I was skeptical showing the typical inertia to change. I still have an objection to keeping the product backlog on Post-it notes (fire?) my initial objections were largely resolved:

How could you develop software without significant upfront specification and design? (Scrum doesn't say don't design, it says don't waste time creating beautiful specifications?)

How can you always develop something useful in a sprint when some features might take 1 person-year to be meaningful? (Scrum doesn't say you ship after each sprint, so you develop large "features" over multiple sprints, each one producing a completed part of the larger feature.)

But I still have three questions that remain unanswered:

1. Scrum aims to create defect free code ([something I'd love to see](/blog/bugs-are-toxic)), but what about products that already exist with a significant number of defects? When do you fix these existing defects? What is the user story?
2. Scrum aims to produce unit-tested code, but what about products that are currently not unit tested? I know from experience making code amenable to unit testing is a time-consuming process. How can you produce potentially shippable software at the end of each spring when the majority of the software is not unit tested?
3. Are there projects that are not amenable to scrum? For example, suppose you wanted to make an existing project available on a new platform (as a Mac user, I want to use product X on a Mac). Suppose too that you decide to migrate from a single-platform UI library (e.g. MFC) to a cross-platform UI library (e.g. QT) in order to share as much code as possible between platforms. How would you approach this with scrum?

I think the answer to the first two parts is to retain alpha and beta phases until quality and test coverage improve. I don't mean that you abandon creating potentially shippable software at the end of each sprint, but recognize the reality of legacy software. However, because the quality of all new features is potentially shippable at the end of each sprint, the alpha and beta phases can be significantly shortened.

While I have a practical solution to my first two questions, I don't have an answer to the third question.