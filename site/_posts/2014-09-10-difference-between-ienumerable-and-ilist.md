---
layout: post
title: Difference Between IEnumerable and IList
date: 2014-09-10
---

During a code review, I recommended changing a return value from `IList` to `IEnumerable`. Is there any real difference between these two interfaces?

In fact, there is one huge difference. `IList` (and `ICollection`) both support insertion to and removal from the collection. When you return these interfaces, you are saying:

> Here's a collection of items. You can modify the items and the collection itself.

The owner of the collection has no easy way to know if the collection has been modified (`ObservableCollection`).

In contrast, `IEnumerable` doesn't support insertion to or removal from the collection. The collection itself is immutable. When you return this interface, you are saying:

> Here's a collection of items. You can only modify the items.

That's a big difference, especially if the owner of the collection needs to know if the collection itself is modified. Unless performance considerations (for direct indexing) trump maintainability, I prefer to return `IEnumerable` for collections.