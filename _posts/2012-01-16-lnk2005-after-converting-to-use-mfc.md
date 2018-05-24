---
layout: post
title: LNK2005 After Converting to Use MFC
date: 2012-01-16
---

Although I work on a large MFC based project, often I create small independent projects before converting and integrating that code into our main product. I usually don't turn on use of MFC until integration of the project because most of the low-level work I'm doing doesn't use MFC.

After integrating the code, I need to turn on use of MFC in order to integrate with the rest of the product, and this invariably causes linker errors:

```
error LNK2005: _DllMain@12 already defined in X
fatal error LNK1169: one or more multiply defined symbols found
```

There is [lots of information about how to solve this](http://support.microsoft.com/default.aspx?scid=kb;en-us;q148652), but these solutions never solve the problem. For my workflow, the solution is to remove the preprocessor definition

```
_USRDLL
```

Hopefully next time, I'll remember this post and not spend half a day trying to identify the problem.