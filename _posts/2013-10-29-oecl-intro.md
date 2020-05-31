---
layout: post
title: Open EDA Component Library Introduction
date: 2013-10-29
---

Finally I can talk about the longest and biggest project I have ever worked on: OECL.  So what is it? Well, let's start with the name.

OECL stands for Open EDA Component Library and it is NI's way of importing component information into Multisim. Quite honestly, I made up the name and no one ever objected, but you can get a lot from the name itself.

OECL is a file format to describe components used in the manufacture of PCBs. That's where the "EDA component library" parts come in. It describes

* symbols for schematic capture,
* packages for PCB layout,
* SPICE simulation models,
* ordering and obsolescence information,
* and components.

It is a single XML format to describe an entire library of EDA components.

It's also open. We went to painstaking efforts to not make it specific to any product from National Instruments, and even included features to specifically enhance compatibility with competing products. There are features that are beyond the capabilities of current National Instruments products but that simply make logical sense. I can't recommend that you use it for other products, but I don't see anything stopping you.

*Note* For full disclosure, the copyright might pose a little problem. If it does, contact me, and I can work with you to see if we can resolve the issue.

That's actually not the only way the format is open. OECL is built on existing standards. That means graphic symbols are written in SVG. You can copy the SVG parts into a separate document and open it up in any SVG viewer. Packages are written in IPC-2581A. In this case, it is a little more complex because IPC-2581A isn't designed for this purpose, so it is more like IPC-2581A+, but the idea is exactly the name. Reuse.

The format is documented, and it is documented well. A company is already working on exporting to OECL using the documentation we created. When they had questions or did things incorrectly, we responded by clarifying the documentation. In the end, we hope that the documentation is very useful. And if it isn't, we'll clarify things.

Not only that, we wrote the code to be shared. If you want to output files in this format, we have a library that can save you a lot of effort. Again, contact me, and I can work with you to see if we can share this with you.

Over the next few posts, I'll give a walk through of the OECL format piece-by-piece. My hope is to explain some of the why and how to avoid some of the traps. In the end, I hope these posts will become the unofficial guide to OECL.

Finally, please contact me if you are looking to use this format. I personally authored the format (with a lot of feedback) and can answer any question related to OECL better than anyone else. I can also provide advice to check if you are correctly authoring files.