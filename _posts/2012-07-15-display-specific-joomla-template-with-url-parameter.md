---
layout: post
title: Display Specific Joomla Template with URL Parameter
date: 2012-07-15
---

For some reason, finding this took an enormous amount of time today. I started writing my own Joomla template, and wanted to see my site in it, without changing my site for everyone else. I knew there was a way to do this with a URL parameter. It is really simple, and I am still annoyed with myself for not just guessing. If you want to see a page with the name `my_template`, append to the URL `template=my_template`.

For example

```
http://www.example.com/?template=my_template
```