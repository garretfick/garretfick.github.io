---
layout: post
title: Beware of wcstombs
date: 2011-12-04
---

Different character encoding schemes are a headache - a headache that is unfortunately not going away. [`wcstombs`](http://www.cplusplus.com/reference/clibrary/cstdlib/wcstombs/) (or related Microsoft secure functions, [`_wcstombs_s`](http://msdn.microsoft.com/en-us/library/s7wzt4be(v=vs.80).aspx) and [`_wcstombs_s_l`](http://msdn.microsoft.com/en-us/library/s7wzt4be(v=vs.80).aspx)) are your staple when translating between wide character and multibyte encodings.

However, wcstombs can have some very unexpected behaviour, when it comes to substitution characters. At least on Windows, this behaviour depends on the system locale.

What's a substitution character? Consider the wide character string

```
wchar_t* str = L"Ê";
```

When will `wcstombs` successfully convert the string? As you might expect, that will depend on whether there is a representation for Ê in the code page. Perhaps unexpectedly, for some code pages, Ê is converted to E. The function succeeds, but [`mbstowcs`](http://www.cplusplus.com/reference/clibrary/cstdlib/mbstowcs/) will not convert back to the original string.

If this is a problem, use `WideCharToMultiByte` with the flag `WC_NO_BEST_FIT_CHARS` and check the return value for `lpUsedDefaultChar`, for example,

```
wchar_t* strIn = L"Ê";
char strOut[2];
BOOL bUsedDefaultChar;
WideCharToMultiByte(CP_ACP, WC_NO_BEST_FIT_CHARS, strIn, -1, strOut, _countof(strOut), NULL, &bUsedDefaultChar);
if (bUsedDefaultChar) {
   //Character not in code page
}
```