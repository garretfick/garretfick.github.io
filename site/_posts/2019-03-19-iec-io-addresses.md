---
layout: post
title: I/O Address Format
date: 2019-03-19
---

OpenPLC uses a particular format for binding variables to addresses. It took a bit of digging around,
but I've finally figured out what they mean and how OpenPLC interprets the addresses. The first part
is to define a general identification for types:

| Data Width  | Input  | Output | Memory |
|-------------|--------|--------|--------|
| Bit         | `IX`     | `QX`     | ~~`MX`~~ |
| Byte        | `IB`     | `QB`     | ~~`MB`~~ |
| Word        | `IW`     | `QW`     | `MW`     |
| Double word | ~~`ID`~~ | ~~`QD`~~ | `MD`     |
| Long word   | ~~`IL`~~ | ~~`QL`~~ | `ML`     |

Items with a strike-through are not currently supported. There is another important note. These values
should indicate the data width (not the type). However, as far as I can tell, OpenPLC assumes
data types based on the definitions, which means you don't have freedom to use they as containers.

(I'm not 100% sure that my understanding of IEC 61131-3 is correct since I only have a book rather
than the original specification).
