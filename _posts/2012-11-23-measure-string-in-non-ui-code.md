---
layout: post
title: Measure String Extent in non-UI Code on Windows
date: 2012-11-23
---

A common problem I've had is measuring text (strings) that will be drawn to the screen from code that knows nothing about drawing. The problem is that the measure text functions expect a device context (an HDC), something you won't have in non-UI code.

I've finally found a way to make this work, although I can't say that it doesn't create a device context. In fact, I have no idea how it works since I can't step into the code, so it might be creating a device context for me. In any case, it is only a few lines of code.

```
using namespace Gdiplus;
Bitmap dummyImage(1, 1);
Graphics canvas(&dummyImage);
WCHAR string[] = L"Measure Text";
Font font(L"Arial", 16);
PointF origin(0.0f, 0.0f);
StringFormat format;
RectF boundRect;
canvas.MeasureString(string, 12, &font, origin, &format, &boundRect);
```