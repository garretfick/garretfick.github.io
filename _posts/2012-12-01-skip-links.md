---
layout: post
title: Skip Links
date: 2012-12-01
---

An earlier post of mine describes the purpose of skip links. Now that you want to implement it, what is the best way? Searching online gives lots of options and an equal number of exceptions. What actually works?

After testing various options, I use the following HTML on my website. The HTML is simple, and the skip link is the first item following the body.

```
<body>
<a href="#maincontent" class="skip">Skip to content</a>
...
<div id="maincontent">
...
</div>
...
</body>
```

The CSS ensures that the link normally doesn't show. The key thing it to make sure that the link does show when it gets focus/activate, otherwise it won't be read in some cases. My CSS is

```
a.skip
{
position: absolute;
left: -999px;
}
a.skip:focus,
a.skip:hover,
a.skip:active
{
left: 5px;
}
```

The important part is the testing. This wasn't my first approach, but it was the first and simplest that works in all scenarios I tested. This approach works in at least the following cases.

<table border="0" summary="Whether this approach works using some operating systems, screen readers, and brower combinations.">
<tbody>
<tr><th scope="col" abbr="os">Operating System</th><th scope="col" abbr="reader">Screen Reader</th><th scope="col">Browser</th><th scope="col">Status</th></tr>
<tr>
<td>Mac Lion</td>
<td>VoiceOver</td>
<td>Safari</td>
<td>OK</td>
</tr>
<tr>
<td>Mac Lion</td>
<td>VoiceOver</td>
<td>Chrome</td>
<td>OK</td>
</tr>
<tr>
<td>Windows 8</td>
<td>NVDA 2012.3</td>
<td>Internet Explorer 10</td>
<td>OK</td>
</tr>
<tr>
<td>Windows 8</td>
<td>NVDA 2012.3</td>
<td>Chrome 23</td>
<td>OK</td>
</tr>
</tbody>
</table>

For things not in the table, such as Firefox, Android, iOS, etc, I simply don't know. If it works (or if it doesn't) let me know and help me populate the table.