---
layout: post
title: Why Should You Prefer Streaming to Buffers?
date: 2012-12-04
---

I've been working with the [xmlwrapp library on GitHub](https://github.com/vslavik/xmlwrapp) for parsing XML in C++. For parsing XML, it provides two interfaces. The first one takes a file name and the second takes a buffer.

For unit testing, I asked one of our interns to add an interface that uses a `std::istream`. When unit testing, we'll just pass in the stream. When not unit testing, we'll construct the stream using the file name and pass it to the parser. In both cases, we'll construct the parser using the `std::istream` ensuring that our unit tests exercise the same code path as production code.

The question then became about implementation. Although there is example code for the buffer, I suggested that we should use the libxml2 streaming interface functions. The intern asked what is the advantage of the streaming interface, particularly since it is more complex? The answer is it's all about memory, and there are two advantages.

## Peak Memory Footprint

An XML DOM contains a lot of text, so it's memory footprint will be similar to the size of the file. If you first read into a buffer, your peak memory footprint will be the twice the size of the file (one for the buffer and one for the DOM). In comparison, when streaming, your peak memory footprint will be the size of the file (just the DOM).

With streaming, you'll simply need less memory.

## Contiguous Memory Footprint

While that's important, the second advantage is where you can really see the difference. If you want to read the contents of a file to memory, then you have to allocate enough contiguous memory for the file. If the file is 10MB, you need 10MB of contiguous memory. A 100MB file needs 100MB of contiguous memory, and so on. Large files are very likely to fail to load. In comparison, when streaming, you only need a small buffer, avoiding any large chunks of memory. The file can be 10 GB, and you'll still be okay in terms of memory because it's all in small pieces.