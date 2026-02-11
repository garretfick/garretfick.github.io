---
layout: post
title: Refactoring My Information Diet - Moving from Push to Pull
date: 2026-01-01
---

As a Principal Engineer, my job is largely about pattern recognition. To spot trends in distributed systems or operational excellence, I need high-quality inputs. But recently, my input stream—emails, newsletters, podcasts—had become a DDoS attack on my attention.

I try to practice Inbox Zero, but the sheer volume of information (newsletters, notifications, automated reports) made this impossible without spending hours on manual garbage collection. I was spending too much time managing the queue than actually learning. I knew I was missing out on some good sources because I was at capacity.

So, I decided to treat my information consumption like a legacy system that needed a re-architecting. I moved from a "Push-based" system (where everything fights for attention in my Inbox) to a "Pull-based" system with strict filtering layers.

## The Architecture

The core philosophy is **Separation of Concerns**. I had designed my email inbox as my one-stop information hub.
I worked to get this empty, but things were getting lost. I've decided to change so that my 
email inbox is for asynchronous communication with humans; it is not for reading, listening, or storage.

## Step 1: The Facade Pattern (Decoupling Subscriptions)

I use Office 365 Business Standard, and previously, I subscribed to newsletters using my primary email alias. This was a mistake. It coupled my personal identity to hundreds of external lists, making "unsubscribe" a manual, per-sender battle.

**The Fix: A Shared Mailbox** Instead of a simple alias, I created an M365 Shared Mailbox (inbox@example.com).

Why: Shared mailboxes have their own storage and inbox but don't require a paid license. They act as a "Demilitarized Zone" (DMZ).

The Flow: I subscribe to everything using this address. It auto-forwards to my reading tool (Readwise) and keeps a local copy as a backup.

The "Gotcha": Microsoft defaults to blocking external forwarding to prevent data exfiltration. I had to drop into
PowerShell to bypass the OutboundSpamFilterPolicy for this specific mailbox, treating it as a trusted relay. I also
configured a retention rule to automatically delete emails after 30 days.

## Step 2: The Firewall (Server-Side Filtering)

For the emails that do hit my main inbox, I stopped trying to manually triage them. I'm pretty diligent about
unsubscribing from legitimate sources, but I still receive a lot of "Greymail" (notifications, receipts, marketing)
that I want to treat differently

**The "List-Unsubscribe" Rule** I created a server-side Exchange rule that inspects message headers—not the body text.

Logic: If Header contains "List-Unsubscribe" -> Move to folder "Grey Mail"

This single regex rule instantly reduced my daily notification volume by ~80%. It catches most marketing spam without me needing to maintain a blocklist. I check the "Grey Mail" folder once a day, unsubscribe, batch-delete the junk, and zero 
it out in seconds.

## Step 3: Standardized Responses (The "API" Approach)

One of the biggest leaks in my day was responding to "Common Inbound" queries: recruiters, vendor outreach, or generic internal requests. I was hand-crafting unique responses to identical queries.

I now treat these interactions like an API request: Identify Intent → Return Standard Object.

I use text expansion tools (Templates in Outlook Web, Text Shortcuts on Android) to map short triggers to full, 
professional responses.

* The Trigger: ;rec (for recruiters) or ;no (for vendors).

* The Payload: A pre-written "Reverse Screen" that clearly states my hard criteria (Role Level, Tech Stack, Comp) or a polite-but-firm refusal.

This turns a 5-minute distraction into a 3-second operation, ensuring I remain responsive without breaking flow.

## Step 4: The Consumption Layer (Active vs. Passive)

I stopped reading in Outlook. Outlook is designed for replying, not reading.

For Text: Readwise Reader The Shared Mailbox pushes all technical content (LeadDev, Distributed Systems blogs) to Readwise Reader.

The Benefit: It bundles newsletters, RSS feeds, and EPUBs into a single clean interface.

AI Integration: I use the built-in "Ghostreader" to summarize long architectural posts. I can ask, "What are the
trade-offs mentioned in this article?" before I commit to reading the whole thing.

For Audio: Snipd I replaced my standard podcast player with Snipd.

The Feature: It uses AI to generate chapters and transcripts for every episode.

The Workflow: I can look at a 2-hour podcast, see that "Minute 45" covers the specific topic I care about, and jump straight there. It turns passive listening into active referencing.

## Next Steps: If This Isn't Enough

This architecture solves the volume problem, but it doesn't solve the relevance problem. If I subscribe to a high-volume feed (like Hacker News or the AWS Blog), I still get 50+ items a day in Readwise.

If this "Phase 1" setup eventually fails to keep up, my contingency plan is Phase 2: The AI Proxy.

I will inject a custom filtering step between the Source and Readwise:

* Extract: A Python script (running on AWS Lambda) polls my RSS feeds.

* Transform: It sends the title and summary to a lightweight LLM with a system prompt: "Rate this article 1-10 on relevance to Distributed Systems and Rust."

* Load: Only items scored >7/10 are pushed to the Readwise API.

This would effectively move me from a "Smart Feed" to a "Hyper-Curated Feed," ensuring that zero noise ever reaches my
reading queue. But for now, the "Phase 1" architecture has successfully restored my sanity.