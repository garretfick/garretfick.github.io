---
layout: post
title: What Makes a Good Standard Operating Procedure
date: 2024-10-06
---

## What is a Standard Operating Procedure?

In software operations, we use standard operating procedures (often called runbooks)
to describe how to mitigate issues. These are procedures to mitigate issues
that we anticipated in advance but lack an automated mitigation.

In my mind, a runbook is a collection of standard operating procedures. There is a collection
of them, which is what makes the collection a run-BOOK. Although I prefer the term SOP,
the term runbook is also commonly used.

## SOP Quality

SOPs are frequently used to mitigate issues under stress. There may be customer
impact. Engineers executing the steps may have been working on the issue for some time
before identifying the right procedure. Leaders want to know how long until the issue
is mitigated and business is back to normal. Sometimes impact has not yet occurred,
but there clear timeline after which impact will begin.

The quality of the SOP can affect the outcome. The responders will not execute the
steps if they cannot identify the right procedure. Alternatively, they might choose
to not follow the steps if they don't believe the steps are accurate or if they
believe that the steps could make a bad situation worse. With that in mind, I think
there are two essential ingredients that differentiate a quality SOPs from the rest.

First, quality SOPs **create** trust so that the responders
believe executing the steps will resolve the particular issue. Trust requires
that we take intentional trust-building actions. For example, you can create trust
by making it clear the last time an SOP was executed or by describing how you
know this is the right SOPs to follow (or both).

Second, quality SOPs are **straightforward**
to follow so that responders take the intended actions. Similarly, making
an SOP straightforward to follow requires intentional actions. For example,
you can make an SOP easier to follow by structuring in a well-known format.

## An SOP Template

The teams I work with use a common template to structure SOPs. This template
grew organically based on real-world experience responding to SOPs.

There are three sections in our SOPs:

* preamble
* steps
* testing

The preamble answers some key information about the SOP:

* what kind of issue the SOP mitigates
* what happens if we were to ignore the issue highlighted
* what is the worst that could happen by following the steps
* how long the steps take to execute
* the last time the steps were followed (due to testing or responding to an incident)

We do this in a brief table so that the information is easy to find and
to discourage ourselves from writing long descriptions.

I feel like this is stating the obvious, but the steps describe the steps.
That said, there are three parts to our steps:

* *check* to confirm that this is the right SOPs to follow
* *act* to perform the steps
* *verify* to confirm that the actions had the desired result

Each of these is described as a numbered list to make it easier to communicate
to others where we are in the steps. The [Microsoft Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/)
is a great for additional information how to to write the actual text in a procedure.

Now, what does our template actually look like.

> ## Preamble ##
>
> | Summary | Describe the issue that this SOP resolves. The purpose is to help identify whether this is the right SOP to use. |
> |---------|--------------------|
> | Why does this matter | Describe what would reasonable happen if the issue is not resolved. Incidents can happen in the middle of the night, on weeks, etc. The purpose is help responders understand whether they should run the steps now or whether they might wait until another times. |
> | What might go wrong | Describe what could reasonably go wrong. Running SOPs have some risk. The purpose is to help responders understand what are the risks of this SOP. |
> | Time to mitigate | Describe how long it takes to execute the steps and observe that the steps have been successful. The purpose is to communicate to stakeholders how long they can expect to wait before seeing a resolution. |
| Last run | Describe the last date that that SOP was either used during an incident or tested. The purpose is to communicate the correct level of confidence in the procedure. |
>
> ## Steps
>
> ### Check
>
> Describe, as a numbered list, the procedure to check that this is the right procedure to run. Very often
> this means identifying the monitors that should be be in alarm.
>
> ### Act
>
> Describe, as a numbered list, the procedure that will resolve the issue.
> 
> ### Verify
>
> Describe, as a numbered list, the procedure to verify that the issues is resolved and that the system
> is in the right new state.