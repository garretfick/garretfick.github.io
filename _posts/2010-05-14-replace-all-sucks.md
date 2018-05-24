---
layout: post
title: Replace All Sucks
date: 2010-05-14
---

We all know, at least programmers, about replace all. It allows you to replace all text in a document that matches some condition, for example, replace all instances of “foo” in a document with “bar.” The problem is that often you inadvertently replace something unintended. “Food” might become “bard” but that may not be my intention. (Of course there are regular expressions and other options, but that ultimately doesn’t solve the fundamental problem.)

Replace all is an exercise in context. “foo” describes part of what I want to replace, but it may match other cases. When I do a replace all, I ultimately want to know, did my description “foo” match only the cases I  want to replace, and ignore the rest? Some programs provide some information to help answer this question, usually in the form of reporting how many were replaced. If the number seems reasonable, you assume it was successful, but you don’t really know, and there is no easy way to figure it out. The problem is the number of items replaced is a piece of data, but it isn’t really useful. Its a common problem we all encounter, data is not necessarily very useful.

This is exactly the problem we were discussing at work today. It's a disagreement I haven’t won yet, usable information will ultimately prevail. Why am I so confident? Because I thought of this great comparison or example that I will use next time we meet. It’s so great, I just had to share it.

Suppose I creating a rudimentary text program. I have this great idea for a new feature I’m going to call “find.” When customers use this feature, then enter a word, say “foo,” the program outputs to the user the number of times that occurred. If I want to replace “foo” with “bar,” I now know to keep looking until I find X instances. Certainly better than me searching blindly. The feature is giving me a piece of data, but is it useful? Not really. I can make the feature a little better. When I search for “foo,” the program can tell me it found “food” 5 times, and “football” 4 times. Now I have a little more data because I know what to look for. Still through, it is not very useful because I have to search through the document. I can improve the feature even more by having it highlight the items for me. Still data, but the data is now useful. There is enough data that software had really done the work for me – it is in a form I can directly use.

In software, data is all over, so it is really easy to display data. But so often, it is only data, and it is not in a form that is useful. It takes a little more thought and work, but the payoff is enormous. For that reason, I’ll win this one, because I won’t accept just displaying data.