---
layout: post
title: OpenPLC DNP3 Master Mappings
date: 2019-03-08
---

_This post describes the model of the world as I currently understand it.
I don't guarantee my model is right, but it is useful._

OpenPLC supports DNP3 on the SoftPLC platform (except for Windows). This post describes how I was
able to interact with the DNP3 slave (outstation) running on Linux SoftPLC. This post follows the
same work I did with Modbus, but using DNP3.

The first thing to note is that we cannot use bidirectional registers. You need to separate inputs
and outputs since that's what DNP3 requires. No more fudging. This means updating our design to 
properly designate binary inputs (1) using `%IX...` and binary output statuses (1) using `%QX...`.

Update the design as follows:

| Name  | Location | DNP3 Group | DNP3 Variation | DNP3 Index |
|-------|----------|------------|----------------|------------|
| `PB1` | `%IX0.0` | 10         | 2              | 0          |
| `PB2` | `%IX0.1` | 10         | 2              | 1          |
| `LED` | '%QX0.0` | 1          | 2              | 0          |


