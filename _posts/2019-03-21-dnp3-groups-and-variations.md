---
layout: post
title: DNP3 Groups and Variations
date: 2019-03-21
---

I'm trying to communicate with the OpenPLC Linux SoftPLC via pydnp3. In this setup
the SoftPLC is operating as the outstation and my code in pydnp3 is operating as
the master.

There are a few ways that you can do a on-shot read from the device (remembering
that all reads are async). The documentation for pydnp3 says something like the following:

| Function         | Usage                                                           |
|------------------|-----------------------------------------------------------------|
| `Scan`           | A scan using a vector of headers.                               |
| `ScanAllObjects` | A scan for all objects with the specified group/variation pair. |
| `ScanClasses`    | A scan for all matching classes.                                |
| `ScanRange`      | A scan of all objects with the specified group/variation pair between indices. |

To understand what these actually do, we need to get through the jargon.

## Jargon

*Point Types*

There are several important point types

* binary input
* analog input
* counter input
* binary (status) output
* analog (status) output

which we can see some are inputs and some are outputs, but it is important to recognize
that your view of whether something is an _input_ or _output_ depends on your frame of
reference. Our frame is that of the DNP3 master. In general, we read from inputs and we
write to outputs.

* Indices*

For each of the point types, DNP3 supports multiple instances. These instances
are identified by a zero-based index. In some contexts, this is called the point number.

*Group*

Groups tell you something about the characteristics of the point type at the specified index.
That is, binary input at index 2 might report itself in multiple ways, for example a current
or frozen value. It could also be descriptive of the value - for example the number of binary
outputs or the maximum binary output index. So, the group gives a semantic meaning to the data.

*Variation*

Another consideration is the variation. Variations tell you about the encoding of the value.
In general, you can think of this as being the data type (e.g. a 16-bit integer), but DNP3
supports a more diverse set of encodings than what software developers are normally familiar with.
The particular set of variations depends on the group, so you don't have freedom to choose them
arbitrarily - you need to select the correct pairing.

## Reading

How that we can understand the jargon, we can talk about reading from the device. Suppose we
want to get the current (also know as _static_) value of a binary input at index 2. How do
we specify that for DNP3?

There is no direct way to specify "binary input". Instead, it is inferred by the group. The
simplest way we can do this is group 1, variation 1. The group selects binary inputs and
the variation selects only the binary value.

If we want read an analog inputs encoded as 32-bit signed integers, then that is group 30
and variation 1. An analog input encoded as double precision is again group 30, but this time
variation 6.

A description of valid combinations of group and variation occupies a small (insert sarcasm)
300+ pages of the DNP3 specification. The high quality [OpenDNP3](https://github.com/automatak/dnp3)
has a partial list, but it is far from complete. Despite this, the industrial applications
I've seen only use a few combinations.
