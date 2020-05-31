---
layout: post
title: Should You Use DATE_LONGDATE or DATE_SHORTDATE?
date: 2013-02-13
---

The Windows API provides the [`GetDateFormat`](http://msdn.microsoft.com/en-us/library/windows/desktop/dd318086(v=vs.85).aspx) and [`GetDateFormatEx`](http://msdn.microsoft.com/en-us/library/windows/desktop/dd318088(v=vs.85).aspx) functions for formatting time information into the appropriate locale specific format. Using the function, you can decide whether to return the date in short format (`DATE_SHORTDATE`) or long format (`DATE_LONGDATE`).

```
// Get the current time
SYSTEMTIME sysTime;
GetLocalTime(&sysTime);

// Where to store the date string
TCHAR szBuf[100];

// Get the date
GetTimeFormat(LOCALE_USER_DEFAULT, DATE_SHORTDATE, &sysTime, NULL, szBuf, sizeof(szBuf)/sizeof(szBuf[0]));
```

The question is then when should you use `DATE_SHORTDATE` and when should you use `DATE_LONGDATE`. For that, we need to look at the Windows User Experience Interaction Guidelines. The guidelines say:

> *Use the long date format for scenarios that benefit from having additional information.* Use the short date format for contexts that don't have sufficient space for the long format. While users choose what information they would like to include in the long and short formats, designers choose which format to display in their programs based on the scenario and the context.

The extremes of additional information and sufficient space are clearly handled. But what should you do when you are outside of these extremes?

I think the answer to this lies in the [Windows User Experience Design Principles](http://msdn.microsoft.com/en-us/library/windows/desktop/dd834141.aspx. The principles tell us to "do less better," and "reduce distractions.". They also ask "are you providing only the necessary steps?" These remind me of the old adage "less is more," or for our question, prefer `DATE_SHORTDATE`.