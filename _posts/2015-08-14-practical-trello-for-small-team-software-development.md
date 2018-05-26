---
layout: post
title: Practical Trello for Small Team Software Development
date: 2015-08-14
---

For small software teams on a limited budget, [Trello](https://trello.com/) can be a really good tool for keeping track of and planning work. Since Trello isn't designed for this task, it gives a lot of flexibility in creating a lean process around it. And I mean really lean - it even works well for an individual software engineer working on a large project. But since Trello isn't designed specifically for the task, a natural first question is what kind of process to create?

This post is all about the process I've created and used in Trello before - the good and the bad - so you can recreate it. I'll try to go into how we actually used it, highlighting some useful attributes that naturally evolve. A decent amount of credit goes to another blog which formed the inspiration for this setup. Unfortunately, I've since lost the link.

When I've set this up before, there were a few of things I want from the process:

1. Bugs and user stories follow a similar process
2. Everything should quickly have a "place"
3. Quickly see relative priority
4. Quickly see a rough time line

It should be pretty obvious from these requirements that they follow a modified [Scrum process](http://en.wikipedia.org/wiki/Scrum_(development)). (Can you call it Scrum at times when I was the only person? Just image the standup meeting.)

Cards And The Boards

Maybe it is already obvious, but in this process, cards represented one unit of work, which was always a bug or a user story. The user story cards might be large (epic) and need further elaboration before starting work, but they nevertheless represented what was currently known.

We arranged things into separate boards so that the boards can be organized according to what the cards represent. I think this really helped in focusing the attention on what was important.

Board       | Purpose
------------|----------------
Current Development | Cards that will be worked on next, are in progress, waiting for testing/evaluation, and the final resting place of all finished work.
Bugs | Bug cards, organized by severity.
Initiatives | Upcoming cards that are tentatively scheduled.
Later | Distant future cards that are being ignoring for now.

## Current Development

This board represented what we were actively working or had worked on recently. Ideally, cards moved from left to right as they go from "up next" to "done", but they can go backwards if needed.

All cards moved through these steps, whether they came from the bug board or a sprint board. In this way, user stories and bugs followed the same process when they are actually worked on.

List               | Purpose
-------------------|---------------------
Up Next            | This was supposed to contain the current sprint's unstarted work. In reality, it became a place where abandoned work rested since it didn't have a better place (see the Initiatives section).
In Progress        | What we were actually working on. Cards often skipped this step, particularly when they were small, and went directly into Testing. That's completely OK and a benefit of a flexible process.
Testing            | Finished cards (code committed) but needing independent verification. Ideally independent verification meant someone else, but it could also mean self testing at a later date. Over the course of a week, this list would grow, and then weekly, we would spend as long as required to check all of the cards. This caught a number of issues, and every week, a couple cards would move backwards in the process.
Evaluating         | Some, but not all of the changes involved A/B testing. This was the holding place for cards there were waiting for enough data to make a decision.
Done               | Truly finished cards. Similar to the Testing list, cards would accumulate here, and then be emptied (Archived). The cadence here, however, was newsletters. Done cards often formed the content for the newsletter, and this gave one place where could see what changed since the last newsletter. Once the list was mined for newsletter items, we archived all of the cards to start fresh.

Looking back, this board worked really well. The Up Next list became a dumping group, but I think that is more a reflection of poor Initiatives boards.

[Example Trello board for Current Development](https://trello.com/b/JKECn1TS/example-current-development)

## Bugs

For bugs, the most useful view is organized by user severity - this is different from importance. The bugs board did just that.

List            | Purpose
----------------|---------------------
Submitted       | The initial state for all bugs. When submitted, the submitter would tag the card with their suggested severity. This initial targeting was useful to help weed through the wording and make sure the cards got appropriately bucketized. Daily (or as much as possible), I would go through this list and move the cards to the appropriate list depending on the importance.

Security/Crash  | Cards in this list could stop development as they were generally considered unacceptable.
Major           | Cards in this list would prevent the customer from being successful. They would not be able to succeed in what they want to do.
Minor           | Cards in this list don't prevent the user from being successful, although they may have to take additional steps to accomplish their goal.
Trivial/Cosmetic | Cards relating to wording, cosmetic issues, layout, etc.

Within each of these, we maintained a marker card, below which all the cards were deferred. The cards below the marker could be ignored on regular basis, and only revisited during a bug blitz or similar activity.

Cards could get one more tag beyond the severity: "customer follow-up required." It was really useful to give this a distinct colour so we could see which cards needed follow when moving from Testing to Done, even without looking at the card details.

One final thing about severity. Why bucketize based on severity and not based on importance or some other dimension? The simple answer is Trello works well for organizing a board based on one dimension, and user severity is relatively objective to evaluate. You want to make it easy to submit bugs and a discussion about importance slows the process and therefore can result in bugs not being entered. You can give bugs priority when moving from Submitted to severity lists by putting the most important at the top.

[Example Trello board for Bugs](https://trello.com/b/zbq7Bp6J/example-bugs)

## Initiatives

Overall, I found tracking user stories in Trello more difficult compared to bugs. It isn't that you can't create cards and organize them. The problem has been evaluating how far away particular stories are away from completion. Yes, everyone knows predicting how long software takes to write is difficult, but there is still utility in knowing how far out a user story is. Is it one month or 6 months out? Should marketing start preparing materials?

My first attempt at an "Initiatives" board had "Submitted", "Approved" lists. Similar to a product backlog, the "Approved" cards were based on priority. But this gave no insight into how much work there was, so it failed that first test.

The next thing I've tried were "Sprint X" boards - essentially dividing the work into week-long sprints. Not surprisingly, initial estimates were not always accurate, some things got added and other things got removed, and in the in the end, we diverged from plan. No problem with that, but I found it time consuming to update the named boards, and eventually, the names weren't so useful. Different developers would be working on different sprints.

What would I try next?

Part of the challenge for the team I worked on was we had a number of interns and I wanted our interns to become specialized in particular areas of the code (to increase their efficiency). In a situation where you cannot treat developers as interchangeable, I again try one board, separated by owner:

List        | Purpose
------------|-----------------
Submitted   | The initial state. Cards from here either get assigned to a particular team member or moved to "Later" if it is too far off to assign.
Team Member A | Ordered cards for A
Team Member B | Ordered cards for B

To solve the "how far away is story X", I propose creating marker cards to identify about 1 sprints worth of work. Then if you want to know how far away a card is, you can count the marker cards. To some degree, list would automatically stay up to date if one card takes longer than expected or work gets added at the top (since the markers would just get pushed down). Other changes would require moving marker cards up or down, but so long as you are planning too far ahead, it should be a small burden.

If you do try this, let me know how it works.

[Example Trello board for Initiatives](https://trello.com/b/YKgH5f6d/example-initiatives)

## Later

The final board, is "Later." Later was the home interesting ideas that we were not ready for, but don't want to completely forget about. All this board has was one or two lists to hold all of the cards and the discipline to periodically review it.

[Example Trello board for Later](https://trello.com/b/M5Rwqgvn.png)

## Summary

That's all there is to it. If you like this process and want to use it for your team, I've setup public boards that you can copy into your team. No setup required.

* [Example Trello board for Current Development](https://trello.com/b/JKECn1TS/example-current-development)
* [Example Trello board for Bugs](https://trello.com/b/zbq7Bp6J/example-bugs)
* [Example Trello board for Initiatives](https://trello.com/b/YKgH5f6d/example-initiatives)
* [Example Trello board for Later](https://trello.com/b/M5Rwqgvn/example-later)