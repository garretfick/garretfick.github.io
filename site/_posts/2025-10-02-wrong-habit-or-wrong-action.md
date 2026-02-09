---
layout: post
title: Wrong Action or Wrong Habit? A Framework for Learning from Failure
date: 2025-10-02
---

There's a curious truth about learning: failure is often a better teacher than success. When something succeeds, the
specific ingredients for that success can be hidden. But when something fails, we can clearly see what didn't work.

I was reminded of this earlier this year after an impactful operational incident. A group of engineers were trying to
make a change in a system. In the process, they authored a procedure, clicked through three distinct warnings that
their action would cause impact, and then proceeded to cause that exact impact. They did all this while firmly
believing, despite the warnings, that the change was only going to affect a different system, thus ignoring
the warnings.

We collectively learned many lessons from that event, but one of the most valuable for me was a simple framework for categorizing the human actions that led to it. During the review, one of the leaders asked me:

> Was it the "wrong action" or "wrong habit?"

## Beyond Blame: Why We Focus on Systems

In modern engineering cultures, we strive to be blameless when incidents happen. We focus on weaknesses in systems and
mechanisms, not people. Blaming individuals is problematic for two key reasons. First, it instills a culture of fear,
which can lead people to hide mistakes. This "normalization of deviance" is a well-documented path to catastrophe, most
famously detailed by sociologist Diane Vaughan in her analysis of the Space Shuttle Challenger disaster. Second, blaming
people implies the problem can be solved simply by hiring "better" people—a fallacy, since we already believed we had
hired the right people for the job.

However, a blameless culture shouldn't mean taking people out of the equation entirely. After all, three people worked
together to take the action that caused the incident. The "wrong action" vs. "wrong habit" model provides a way to talk
about how people contributed to an incident without blaming them.

## Understanding the "Wrong Action"

A "wrong action" occurs when an individual (or individuals) has a clear goal but operates with a flawed mental model
of the system. They use their prior experience, system indicators, and other information to build a picture of how
the system works and its current state. The problem is, that picture doesn't match reality.

When this happens, the person isn't being negligent; they are acting logically based on incorrect information. To
address this, we need to reduce or remove the reliance on individuals having a perfect mental model. This is far
harder than it sounds. It might involve designing systems that refuse to perform an unsafe action or providing much
clearer and unmissable feedback about the true state of the system.

## Understanding the "Wrong Habit"

A "wrong habit" stems from repetition and familiarity. An individual has a goal in mind and has performed this action,
or a similar one, many times before. Because of this, they go on autopilot, acting reflexively and ignoring indicators or
warning signs that they would have otherwise noticed. They've been conditioned to believe the action is always safe.

To address this, we need to look at the culture and the mechanisms that enabled a repetitive, rote culture to develop. The 
solution might involve automating the task to remove the repetition that allowed the habit to form in the first place, or 
introducing variation into the task to force more conscious engagement.

## A Tool for Better Systems

In the scenario I described, the engineers believed the change was going to affect a different system. Their mental model 
of the environment was incorrect, and all subsequent actions were based on that initial faulty assumption.

It was a classic case of the wrong action.

This simple distinction is more than just semantics. It’s a diagnostic tool. It shifts the focus from "Who made a
mistake?" to "What kind of mistake was it, and how can we make our systems more resilient to it?" By categorizing
the failure, we can better target our solutions, building systems that are safer from both flawed assumptions and
mindless repetition.