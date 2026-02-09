---
layout: post
title: Breadcrumbs and Web Accessibility
date: 2012-11-27
---

I've decided to give a talk on web accessibility in a few months, in particular, on how to make web pages accessible. I've spent time trying to make this site more accessible, but until today I never turned on a screen reader.

I have a long way to go!

Let's start with the first thing I learned and implemented. I have breadcrumbs on this site to show your location on the site. I wanted something fast that didn't need lots of styling, so I wrote the breadcrumbs as

```
<ul>
    <li><a href="/">Home</a> ></li>
    <li><a href="/blog">Blog</a> ></li>
    <li>Page title</li>
</ul> 
```

When I turned on [VoiceOver](http://en.wikipedia.org/wiki/Voice-over/), I was horrified to find that my breadcrumb was a list of 5 items, but there are only 3 items in the list. My guess is that VoiceOver is simply counting the number of child elements in the HTML (which turns out to be 5 because of the content I added).

Scratch that idea. The whole idea of putting the separator in the HTML was a bad idea from the beginning - mixing presentation with content. A better approach, and one that works with VoiceOver, is to use CSS to add the separators.

```
<ul>
    <li class="pathway"><a href="/">Home</></li>
    <li class="pathway"><a href="/blog">Blog</a></li>
    <li class="pathway_end">Page title</li>
</ul>
```

The CSS then adds a background image with left padding so the text doesn't overlap the image. The resulting breadcrumb displays like

Home and an arrow, followed by blog and an arrow, etc

![](/static/img/blog/breadcrumbs-and-web-accessibility/breadcrumb_example.png)

The lesson here is: if it's for presentation, keep it in the CSS.