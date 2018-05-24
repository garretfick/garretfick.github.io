---
layout: post
title: Automatically Show Image for Paragraph using CSS
date: 2012-07-14
---

*This is an old post that has been converted to a new format. The original image does not show, but the technique is still valid.*

My experience writing web pages is relatively causal. The first time I wrote HTML was probably in 1997, creating a Geocities page (somehow I still remember it was CapeCanaveral/Hall/3230). I've created lots of web pages since then, but web has never been a primary focus, so I usually have to do a little searching when I want to anything complex with style sheets so this is a note to myself how I did something in CSS.

I wanted to always show an image for a particular type of paragraph, in my case, for notes, like what you see below.

This is a note with an automatic image because of the style.

I didn't want to have to directly reference the image in each page - when I change the image in the future, I don't want to have to edit every page. For web experts, this is probably a no-brainer, but for the rest of us, how did I do it?

I used a non-repeating background image, then added padding and minimum height to make sure the paragraph was offset relative to the image and that the box was big enough that the image wouldn't get cropped.

```
p.fw_note {
 background-image:url(../images/system/note.png);
 background-repeat:no-repeat;
 margin-left:10px;
 padding-left:60px;
 padding-right:40px;
 min-height:40px;
}
```

To use this style, I just add the class to the paragraph

```
<p class="fw_note">Paragraph text</p>
```