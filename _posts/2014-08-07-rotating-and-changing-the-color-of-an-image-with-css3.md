---
layout: post
title: Rotating and Changing the Color of an Image with CSS3
date: 2014-08-07
---

For the menu system on the website I'm working on, we want to have a triangular icon that indicates the item has children. The items themselves are stacked vertically and expand when clicked and so we want to icon to have two states:

* an unopened state, pointing to the right
* an opened state, pointing downward

To make things more interesting, the color of the item changes when expanded, so the color of the triangle should also change. And for one final request, the icon transitions between the states by rotating. Oh, and if possible, I want to use CSS3 - I'm ok if old browsers don't get the animation.

Let's start with what this looks like:

<iframe src="/static/img/blog/rotating-and-changing-the-color-of-an-image-with-css3/click_rotate_animation.html"></iframe>

This is actually quite easy, and you can achieve the effect with only a few lines. You need only

* styles that define the position and how to transition,
* JavaScript to add/remove the appropriate styles

## HTML

The HTML contains the content we want to animate appropriately tagged so we can find it with Javascript and a default class.

```
<a href="#" onclick="toggle_class('img'); toggle_class('sprite');">Toggle arrow</a><br><p><code>img</code> element</p><br>    <img id="img" class="unrotated" src="data:image/png,%89PNG%0D%0A%1A%0A%00%00%00%0DIHDR%00%00%00%14%00%00%00%14%08%06%00%00%00%8D%89%1D%0D%00%00%00%06bKGD%00%00%00%00%00%00%F9C%BB%7F%00%00%00%09pHYs%00%00%0B%13%00%00%0B%13%01%00%9A%9C%18%00%00%00%07tIME%07%DE%08%07%07%2A%27%86i%CBA%00%00%00%0CiTXtComment%00%00%00%00%00%BC%AE%B2%99%00%00%00%5CIDAT8%CB%CD%D4%01%0E%00%20%08%02%40%F1%FF%7F%B6%0F4%05%C7Z%3E%E0VI%A0%AA%2A%8C%93a%9E%2B%08%00%F6%13n%D1%F6%CA%1Bt%7CC%15%A5%96%A2%A0%F4%96YT%8A%0D%83%CA9%9C%D07%C1%EEf%FA%AA%E9%C4%24%90-%91tb%14%A8%D6%5B%3A%B1%16%DC%16%2F%BEo%EC%03%80O%24%238%EB%8E%EF%00%00%00%00IEND%AEB%60%82" /><br><p>CSS image sprite</p><br><div id="sprite" class="unrotated" sprite"></div>
```

First is a link and it calls the `toggle_class` function to initiate both rotation options. `img` and `sprite` are the ids of the elements we're going to animate.

Next are the images we're going to rotate, both an inline image and one references as a CSS sprite is the paragraph we're going to animate. Initially it has the class `unrotated`. You could also omit this, but you'll need some way to specify how to apply the rotation. More on that in a second.

For the inline image, there is a data URI. You could reference an image in the normal way - I've done it this way so that I have a standalone HTML file that you can download.

The images themselves are a little interesting - the images are actually drawing the surrounding, leaving a transparent arrow in the middle. That's because it isn't possible (in this way) to change the image color. Instead, we actually change the background colour and let the background show through the image.

## CSS

The CSS does two things:

* defines classes which identify how to rotate and color the image.
* defines how to transition to those states.

```
#slider
.unrotated
{
    background-color: black;
    transform: none;
    transition-property: background-color,transform;
    transition-duration: 10s;
    height: 20px;
    width: 20px;
}
.rotated
{
    background-color: red;
    transform: rotate(90deg);
    transition-property: background-color,transform;
    transition-duration: 1s;
    height: 20px;
    width: 20px;
}
```

`unrotated` defines the default black arrow (via the background) and unrotated position and how to get to that location from any other position (because it animates the `background-color,transform` properties). `rotated` defines the rotated red arrow (via the background) and how to get to that location from any other position.

When the box moves to `rotated`, it will take 1 seconds to move. When the box move to `unrotated`, it will take 10 seconds to move.

The full CSS also contains the reference to the image sprite.

## JavaScript

The final piece is the JavaScript that initiates the transition. It does this by adding/removing classes. So, when we add the `rotated` class, it rotates and changes the background color. You can of course use a library such as [jQuery](http://jquery.com/) to add/remove, but you can achieve the same effect with just a few lines of code.

```
function toggle_class(elem_name)
{
    var elem = document.getElementById(elem_name);
    if (elem.classList.contains("unrotated"))
    {
        elem.classList.remove("unrotated");
        elem.classList.add("rotated");
    }
    else
    {
        elem.classList.remove("rotated");
        elem.classList.add("unrotated");
    }
}
```

## Fallback

For browsers that don't support animation, they just don't get that part. The location still changes - it just changes immediately.

## Summary

That's all there is to it. If you like this, you can [download the full source](/static/img/blog/rotating-and-changing-the-color-of-an-image-with-css3/click_rotate_animation.html) and integrate it into your website.