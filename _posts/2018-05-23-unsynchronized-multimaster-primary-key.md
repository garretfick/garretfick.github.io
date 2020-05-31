---
layout: post
title: Safe Multi-master Primary Keys
date: 2018-05-23
---

A common database design practice is to use auto-incrementing (unsigned) integers as the primary key for a table.
While there are other approaches, such as UUIDs (GUIDs), integers have several advantages:

1. reduces memory footprint per item
1. smaller database indices
1. easy to query (compare to encoded UUIDs)

However, they do have a significant disadvantage compare to other solutions if you have multiple masters.
The auto-incrementing integer must be unique, and if you have multiple masters, you need to ensure that
both masters don't create the same value - that is, the database must synchronize on every insert.
This synchronization defeats part of the purpose of allowing multiple masters.

It is possible to have non-overlapping auto-incrementing keys without synchronization on every insert?

Yes - use custom sequences to increment by more than 1 and then set each master with a different starting point:

| DB A | DB B |
|------|------|
| 1    | 2    |
| 11   | 12   |
| 21   | 22   |
| 31   | 32   |

In PostgreSQL

```sql
CREATE TABLE currentvalues (
idcurrent bigint primary key
CREATE SEQUENCE currentvalues_seq INCREMENT 10 OWNED BY currentvalues.idcurrent USING local;
ALTER TABLE currentvalues ALTER COLUMN idcurrent SET DEFAULT nextval('currentvalues_seq');
SELECT setval('currentvalues_seq', 1);
```

The second master is similar, but has a different starting point

```
SELECT setval('currentvalues_seq', 2)
```

Disadvantages? You will exhaust the possible values sooner and you have to maintain this stateful information,
particularly through restoring from backups.
