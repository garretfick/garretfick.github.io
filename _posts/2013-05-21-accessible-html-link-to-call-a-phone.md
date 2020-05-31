---
layout: post
title: Accessible HTML Link to Call a Phone
date: 2013-05-21
---

You can find lots of information about how to create HTML links to call a phone number. The syntax is essentially `<a href="tel:NUMBER">NUMBER</a>`. Most examples however would not work for people with disabilities.

[Screen reader users often navigate links out of context](http://webaim.org/techniques/hypertext/#link_to_link), that is, go from link to link, skipping the text in between, so if you simply write `<a href="tel:555-2106">555-2106</a>`, the screen reader will simply hear "555-2106", and that won't make much sense. To make a telephone link accessible, you need to add context information. One way to do this is to write the link in a phrase, for example `<a href="tel:NUMBER">call Example Organization at NUMBER</a>`. When a screen reader user navigates to your link, they will hear "call Example Organization at NUMBER", and your link will make much more sense.