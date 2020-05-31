---
layout: post
title: Finding an Object Using Lambda Expressions
date: 2012-03-02
---

After a hiatus in XML-land, I'm back developing in C++ land. We've moved to up Visual Studio 2010 since the last time I was doing serious development work, and so I'm getting to try out new new C++ language features. Today was my first foray into lambda expressions. Microsoft has some great examples in their documentation ([Lambda Expression Syntax](http://msdn.microsoft.com/en-us/library/dd293603.aspx) and [Lambda Expressions in C++](http://msdn.microsoft.com/en-us/library/dd293608.aspx)), but I need to do something quite common, but not in their list of examples.

My objective was to find a particular item in a collection matching some criteria. Essentially, it boils down to:

```
class ContainerClass {
   public:
      bool ItemExists(int itemId);
   private:
      struct Item{ int itemId; ... };
      std::vector<Item> _items;
};
```

I want to implement the ItemExists function. Without using lambda functions, you would iterate through the collection, checking for the matching itemId. How can we do this with lambda expressions?

```
bool ContainerClass::ItemExists(int itemId) {
   return std::find_if(_items.begin(), _items.end(), [itemId](const Item& item) { return item.itemId == itemId; }) != _items.end();
}
```

At this point, I'm not sure if this is a good or bad use of lambda expressions. Is the code more clear? What is the performance difference?