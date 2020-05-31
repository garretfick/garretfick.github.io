---
layout: post
title: Messages for Exceptional Errors
date: 2013-02-01
---

One of things I really like about the [Windows User Experience Interaction Guidelines](http://msdn.microsoft.com/en-us/library/windows/desktop/aa511258.aspx) is the expression of error messages. Microsoft phrases this as "problem, cause, solution." In fact, the idea isn't new, and you can find similar working in the [Apple Human Interface Guidelines](https://developer.apple.com/library/mac/#documentation/UserExperience/Conceptual/AppleHIGuidelines/Intro/Intro.html), which talks about "what, why, options." The messages aim to provide the customer with all the information they need to proceed.

But are there are limits to when you should provide this complete information? Crafting these error messages takes time, especially when you consider that these messages must also be translated into multiple languages. In a world of constrained resources, I think there are a class of error messages where you can provide less than complete information.

## Exceptional Errors

Some types of errors are quite exceptional. For example, I've seen a lot of code that checks whether a fundamental part of Windows is installed, such as `RICHED32.DLL`. The absence of this DLL is a serious problem, and it's reasonable to assume that Windows would not be running without this DLL. I don't think it is valuable to write a detailed error message for this type of exceptional error, and how would you phrase the solution?

> Unable to edit the text because `RICHED32.DLL` do not exist. Reinstall Windows and this program, then try again.

The same can be said for parts of a product's installation. If a required part of the product is missing, is it valuable to provide a specific message for each case? A failed installation should be indicated by a message from the installer. They would have already received an appropriate error message.

## Messages for Exceptional Errors

For errors that are so exceptional that it's surprising the product is even running, it makes sense to reduce the work and give a common error message. In case you were wrong and it isn't that exceptional, you should an additional identifier to uniquely identify the message to assist technical support.

> PRODUCT encountered a problem caused by an incorrect installation. Reinstall or repair PRODUCT to resolve this issue. Problem code: ABC123

Going one step further, you could even make the problem code clickable so that it goes to the products website, and either shows an appropriate KB article for the unique code or automatically logs an error for problem codes that haven't been previously reported so that you can create the appropriate KB.

Problem codes should be easy to create, and ideally, require no work on the part of the developer. It should be similarly easy to decode the problem code and identify exactly where in code the error occurred. In C++, you have two macros, `__FILE__` and `__LINE__` to help you. Use a using a hash function to convert the `__FILE__` macro into a number (omit everything but the file name), add a dash, and then the `__LINE__` macro.

```
#define MAKE_GENERAL_ERROR(file, line) \
   std::ostringstream sstr; \
   my_hash(file) << '-' << line; \
   return sstr.str();
 ```

Your code then becomes something like the following.

```
if (!found_riched)
{
   handle_error(MAKE_GENERAL_ERROR(__FILE__, __LINE__));
}
```

If you ever need to identify this error, you can easily write a script to calculate the hash for all files, and then lookup the file like a dictionary.