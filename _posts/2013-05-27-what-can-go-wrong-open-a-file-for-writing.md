---
layout: post
title: What Can Go Wrong Open a File for Writing
date: 2013-05-27
---

During a code review, I requested an intern to add a `try-except` block for some file handling code. (The language happen to be [Python](http://python.org/), but that isn't really the point.) He had written

```
in_file = None
out_file = None
try:
    in_file = open(in_file_path, 'r')
except IOError:
    print 'Cannot open input file ', in_file_path
    return -1
out_file = open(out_file_name, 'w')
```

There was a `try-except` for the input file, but not for the output file. He asked me "What could go wrong, so why add the `try-except`"? Actually, quite a few things could go wrong.

* `out_file_name` may not be an allowed file name, for example my?Name.
* The directory path may not exist or may not be allowed.
* The file might already exists, and be opened in another application with exclusive write access (which denies the write access).
* The user might not have create or write permission for the directory.

A lot of things can go wrong when trying to open a file, and depending on your error handling strategy, you need to be prepared to catch those exceptions.