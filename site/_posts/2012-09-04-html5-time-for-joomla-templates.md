---
layout: post
title: HTML5 time for Joomla templates
date: 2012-09-04
---

HTML5 has a new [`time`](http://www.w3.org/TR/html5/the-time-element.html#the-time-element) element. You can use it simply to identify parts of your document that describe a date/time, but the most useful part is you can use it to describe a date/time in a machine readable format using the `datetime` attribute. For example

```
<time datetime="2011-11-12T14:54">Nov 12, 2011 at 2:54 PM</time>
```

You can write the date time in any format, even translate it, but still make the date/time accessible to machines.

Many [Joomla](http://www.joomla.org/)-based sites, including this one, include date/time information for articles, but in most cases, don't use the HTML5 time element.

*Note* Since the `time` element is not part of HTML4, You should only tag content with the `time` element if your template is generating HTML5. You can check that be inspecting the `DOCTYPE` (the first line if you view your site's source). An HTML5 doctype look's like `<!DOCTYPE html>`.

In order to markup your documents with the time element, you first need to find where your template inserts dates. In most templates I've seen, this is somewhere in `<templatename>\html\com_content`. Good places to start include (a good template might have one location, but I've never seen that in while, except for this site):

1. `<templatename>\html\com_content\article\default.php`
2. `<templatename>\html\com_content\category\blog_item.php`

Within those files, search for `item->created`, `item->modified`, and `item->publish_up`. Here, the details will really depend on the template, but one common thing is you'll need to format the date/time into the format expected by HTML5. To do that, use the `DATE_W3C` constant, for example.

```
<?php echo JHtml::_('date', $this->item->created, JText::_(DATE_W3C)); ?>
```

That gets inserted as the `datetime` attribute. For this site, the entire code is

```
<time class="create article-info-item" datetime="">
<?php  $createdate = JHtml::_('date', $this->item->created, JText::_('DATE_FORMAT_LC')); ?>
<?php  $createdate = '<span itemprop="dateCreated">' . $createdate . '</span>'; ?>
<?php echo JText::sprintf('COM_CONTENT_CREATED_DATE_ON', createdate); ?>
</time>
```

The code for the other date/time values is very similar.