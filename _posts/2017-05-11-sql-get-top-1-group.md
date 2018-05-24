---
layout: post
title: SQL To Get Top 1 In Group
date: 2017-05-11
---

A pretty common problem is to get the top N items from a group from a SQL database. For example, suppose you wanted to get the last order for each customer - this is a top 1 item grouping by customer ID.

For some database engines, you can use `OVER` and `PARTITION BY` to achieve your goal. These functions don't exist on MySQL and SQLite, so if you are using those engines, then you need to fall back to basic SQL. It is almost certinally not as efficient (basically doing a cross-product), but you can make it work.

The key insight, described well by [Bill Karwin](http://stackoverflow.com/users/20860/bill-karwin) on [Stackoverflow](http://stackoverflow.com/questions/1442527/how-to-select-the-newest-four-items-per-category/1442867#1442867) is to join the table with itself, but only do the join for the last item.

Suppose the schema of table `items` contains a field for your group (e.g. customer ID) and a unique monotonically increasing field (e.g. the primary key or date)

id | category
---|---------
0  | cat1
1  | cat2
2  | cat1
3  | cat2
4  | cat3

```
SELECT i1.category, i1.id
FROM items i1
# Join the table with itself
JOIN items i2
  # We are joining only those that are the same category (e.g. customer ID) AND then for that, do the cross product
  ON (i1.category = i2.category AND i1.id <= i2.id)
# Then create groups based on the ID and the category ID
GROUP BY i1.category, i1.id
# Finally discard any groups with more than 1 item
HAVING COUNT(*) < 2;
```

Finally, what you really want is the columns, so use that as a subquery to get the data you really care about.

```
SELECT * from items WHERE id IN (
SELECT i1.id
FROM items i1
LEFT OUTER JOIN items i2
  ON (i1.category = i2.category AND i1.id <= i2.id)
GROUP BY i1.category, i1.id
HAVING COUNT(*) < 2);
```