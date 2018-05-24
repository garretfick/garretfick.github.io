---
layout: post
title: pre, code, kbd, samp, and var
date: 2012-10-23
---

HTML has tags that are useful for giving additional semantic meaning to text. They are particularly useful for describing code or instructions for using a computer, although I've rarely seem them used, and I've rarely used them myself. I'm talking about `pre`, `code`, `kbd`, `samp`, and `var`.

I doubt search engines likely don't do anything special for them, but that doesn't mean they aren't valuable. I think they are still highly useful for maintaining a consistent look across a website. And because they have specific and different meanings, they are easy to remember and you can use them for styling without introducing additional CSS classes.

The first thing to note is that they are not equivalent. `pre` is a grouping element, similar to `p`, whereas `code`, `kbd`, `samp`, and `var` are text-level elements. The text-level elements can only occur with the context of a grouping element:

```
<code><p>After typing in <kbd>cd D:</kbd> at the command prompt, the output should show <samp>D:\></samp></p></code>
```

or 

```
<code><pre><code>void main(void) {}</code></pre></code>
```

With that in mind, when should you use these elements?

Element  | Usage | Examples
------------- | -------------
`code`  | A fragment of computer code | XML element names, C++ class implementation, A file name
`kbd`| User input, typically via keyboard or speech | Describing key presses, Command prompt input
`samp` | Program output | Command prompt output, Text from message boxes
`var` | Simple variable | Mathematical variable, Programming variable

If I want to be complete, it is also possible to combine the code `kbd`, and `samp` elements for even more semantically descriptive meanings, but the HTML specification also says such precision isn't necessary. To me, that says don't bother.

Now's your turn to try it out on your own website and document authoring.