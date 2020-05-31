---
layout: post
title: Simple Sliding CSS3 Animation2
date: 2014-03-07
---

The website I'm working on uses a responsive design and the mobile layout has the menu hidden along the side. We want it to slide out when the user clicks the menu button (or swipes). I wanted to do this without using lots of JavaScript and rely on CSS3 with a good fallback for browsers that don't support CSS3.

Since some of you may want to just see the end result before reading further, I'll explain how to create the following animation:

<p><iframe class="html-sample-preview" src="storage/blog/simple_css3_slider/click_slide_animation.html" allowfullscreen="allowfullscreen"></iframe></p>

This is actually quite easy, and you can achieve the effect with only a few lines. You need only

* styles that define the position and how to transition,
* JavaScript to add/remove the appropriate styles

## HTML

The HTML contains the content we want to animate appropriately tagged so we can find it with JavaScript and a default class.

```
<a href="#" onclick="toggle_position('slider');">Toggle position</a>
<p id="slider" class="left-pos">
This is a block that we want to animate<br/>
using CSS3 animations. We use a little<br/>
JavaScript to change the class but otherwise<br/>
it is all in the CSS.<br/>
</p>
```

First is a link and it calls the `toggle_position` function with `slider`. `slider` is the `id` of the element we're going to animate (using a parameter just makes your code a little more reusable).

Next is the paragraph we're going to animate. Initially it has the class `left-pos`. You could also omit this, but you'll need some way to specify how to animate the left-ward effect. More on that in a second.

## CSS

The CSS does two things:

* defines classes which identify how to position the text (sliding in and out).
* defines how to transition to those positions.

```
#slider
{
    position: absolute;
}
.left-pos
{
    left: 0;
    transition-property: left;
    transition-duration: 10s;
    transition-timing: ease;
    transition-delay: 0;
}
.right-pos
{
    left: 100px;
    transition-property: left;
    transition-duration: 2s;
    transition-timing: ease;
    transition-delay: 0;
}
```

`left-pos` defines a location and how to get to that location from any other position (because it animates the `left` property). `right-pos` defines a location and how to get to that location from any other position (because it animates the `right` property.

When the box moves to `right-pos`, it will take 2 seconds to move. When the box move to `left-pos`, it will take 10 seconds to move.

## JavaScript

The final piece is the JavaScript that initiates the transition. It does this by adding/removing classes. So, when we add the `right-pos` class, it changes the location using the specified transition. You can of course use a library such as [jQuery](http://jquery.com/) to add/remove, but you can achieve the same effect with just a few lines of code.

```
function toggle_position(elem_name)
{
    var elem = document.getElementById(elem_name);
    if (elem.classList.contains("left-pos"))
    {
        elem.classList.remove("left-pos");
        elem.classList.add("right-pos");
    }
    else
    {
        elem.classList.remove("right-pos");
        elem.classList.add("left-pos");
    }
}
```