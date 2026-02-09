---
layout: post
title: std::find_if with C-style arrays
date: 2012-12-06
---

It is probably less well known, but many of the C++ STL algorithms can operate on containers and C-style arrays. The evidence is that few examples cover C-style arrays. But C-style arrays are great, particularly when you have static data that is known at compile-time. I'm going to break with the norm and give an example specifically about C-style arrays and `std::find_if`.

We have a table of data, and we want to find an item in that table.

```
struct Item {
   int key;
   int value;
};
const Item kItems[] =
{
   { 1, 10 },
   { 2, 20 },
   { 3, 30 },
   { 4, 40 }
};
```

Now, how do you use std::find_if to locate an item? It's actually pretty straightforward and similar to how you would do it with container classes.

```
int key = 3;
Item* item = std::find_if(std::begin(kItems), std::end(kItems), [key](const Item& item)
{
   return item.key == key;
});
 
if (item != std::end(kItems))
{
   std::cout << "Found: " << item->value;
}
else
{
   std::cout << "Not found";
}
```