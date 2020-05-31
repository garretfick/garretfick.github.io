---
layout: post
title: Delegates Without Objects
date: 2012-12-07
---

Last time I posted about why you should prefer streams to buffers. That post was motivated by some work I asked of an intern. I asked her to use the streaming interface functions with the XML parser instead of allocating a buffer to read in the file.

In our case, we are using [the libxml2 library](http://www.xmlsoft.org/), which has a C API, and that means no objects, and the intern was a little confused about how to use streams in the C API. In fact, libxml2 uses a really common pattern, but since I never formally studied software development, I actually don’t know the name. I’d call it delegates without objects. The pattern can be hard to spot if you haven’t seen it before, so I thought I’d make some pictures while I’m compiling.

The basic condition is some general purpose library needs to ask you do to some work. It asks you to do some work via a callback function or event, and it gives you a "user data" pointer to give the right context.

Suppose the library is an XML parser, and it wants to work with a stream-like interface. During initialization, you give the parser a pointer to a "read" function and the parser will call your function to get more data. In order to know the context, such as which file, you also give the parser a user data pointer that gets passed to the “read” function. Lets put these words to some code, mostly using C.

```
#include <iostream>
#include <sstream>
#include <string>

// ----- Definitions from the general purpose library -----

// This is the C-based XML parser object
struct XmlParser
{
   int dummy;
};

// The read function our parser uses to get more data
typedef int (*xmlReadFn)(void* user_data, char* s, int len);

#define BUF_SIZE 5
// The parse function for our parser
void xmlParse(XmlParser* parser, xmlReadFn read_fn, void* user_data)
{
   char buf[BUF_SIZE];
   int read_len;
   do
   {
      read_len = read_fn(user_data, buf, BUF_SIZE);
      // Here I'm just printing out what we read, one chunk per line
      std::string str(buf, read_len);
      std::cout << str << std::endl;
   }
   while (read_len == BUF_SIZE);
}


// ----- Your code -----


// This is our implementation of the xmlReadFn function
int readFromStream(void* user_data, char* s, int len)
{
   std::istream* str = (std::istream*)user_data;
   return str->readsome(s, len);
}


int main()
{
   // Allocate the parser
   XmlParser parser;

   // Construct the stream we want to read from. Normally, this would come from a file
   std::stringstream str("The quick brown fox ran over the lazy dog.");

   xmlParse(&parser, readFromStream, &str);
   return 0;
}
```

I've also put a [running example on ideone.com](http://ideone.com/4Daryg).