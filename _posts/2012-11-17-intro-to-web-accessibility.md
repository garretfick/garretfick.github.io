---
layout: post
title: Intro to Web Accessibility
date: 2012-11-17
---

I'm at [Intro to Web Accessibility](http://sadecki.com/presentations/a11y-intro/) at [Accessibility Camp Toronto](http://www.accessibilitycampto.org/). I've tried to make my website accessible, so what have I done wrong? I'm sure there is a lot more, but these are the ones I caught during the presentation.

## Omit site name in `<title>`

Screen readers read the page title, which means if you include the website title, the reader will read out your site title every time someone visits your page. It's just annoying. Put the name of the content first, and optionally your site title second, the opposite of my site.

![](/static/img/blog/intro-to-web-accessibility/bad_site_title.png)

## Provide a "skip link"

Navigating navigating links by the keyboard always starts with the first item in the code. Normally we put navigation content first, which means you have to tab through all the navigation items first before you get to the main content. Again, it's really annoying.

An improved way is to provide a "skip link" that goes directly to the main content. To be useful, this link needs to occur before other links and the text should make sense, such as "skip to main content". You can use CSS to position it later, perhaps even off screen, or even invisible until it has focus.

## Provide useful information in links

Links should be understandable out of context. That part isn't new. But you should include all relevant information, including file path and download size. It's really useful to know it's a 1GB download before clicking the link.