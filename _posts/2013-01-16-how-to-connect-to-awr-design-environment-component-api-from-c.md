---
layout: post
title: How to connect to AWR Design Environment Component API from C++
date: 2013-01-16
---

AWR Design Environment has a COM API which you can use to extend the product. COM is easy to use from .NET languages, but requires a little extra work to use from C++, which is usually my language of choice. Before today, I had never used COM with C++, so I had a bit of a learning curve before I could figure out how it works. But in the end, I have something that works, and this would apply for using virtually any COM library in C++.

## Test Out in a .NET Language

Using COM from a .NET language is pretty straightforward. It's much easier to debug issues in C++ land when you know the basics of how the library is expected to work. (This also gives a lot of other useful information that we'll see in a bit.) For that, I started by trying to use the library in C#.

I won't go over the details here, but the basic steps are to add a reference (in this case AWR Design Environment 10), then write some test code. The first thing you need to do to use the AWRDE API is create the application then create a project. In C#, you main function would look like

```
static void Main(string[] args)
{
   MWOffice.Application objMWO = new MWOffice.Application();
   objMWO.New("");
}
```

Running this code should launch a new instance of AWRDE. With that, you know everything is working in COM world.

## Create the C++ Project

Now that we know everything is working from .NET, it's time to try things from C++. I created a simple Win32 Console Application, and left all settings set as default. But now what? If we're going to use an object in C++, we need a header file, but the COM library doesn't include a header file. Thankfully, Visual Studio can create it for us using the type library and the [`#import preprocessor directive`](http://msdn.microsoft.com/en-us/library/8etzzkb6(v=vs.110).aspx).

First, we need to find the type library. Rather than search for the library, our earlier C# application can help us find the type library. From the `Solution Explorer`, select the `MWOffice Reference`. In the `Properties` pane, find the `Identity` property, and copy the GUID.

![](https://s3-us-west-2.amazonaws.com/ficksworkshop/media/blog/how-to-connect-to-awr-design-environment-component-api-from-c/tlb_guid.png)

Next, launch the Registry Editor, and search for that GUID. The default value of the win32 registry key for the GUID gives the location of the type library on your system. In my case, this is `C:\Program Files (x86)\AWR\AWRDE\10\MWOffice.exe`.

![](https://s3-us-west-2.amazonaws.com/ficksworkshop/media/blog/how-to-connect-to-awr-design-environment-component-api-from-c/tlb_location.png)

To use the type library, we add the `#import` directive to the precompiled header (other header files won't work, which if you think about it, actually makes sense). If you haven't made any other changes to the default file created by the project wizard, you'll have the following in `stdafx.h`:

```
#pragma once
 
#include "targetver.h"
 
#include <stdio.h>
#include <tchar.h>
 
#import "C:\Program Files (x86)\AWR\AWRDE\10\MWOffice.exe"
```

Now compile your project. The AWR API generates a few errors and as yet, I haven't tried to figure out why. You can fix the compile errors by adding some attributes to the #import directive. I used the following to resolve the compile errors.

```
#pragma once

#include "targetver.h"

#include <stdio.h>
#include <tchar.h>

#import "C:\Program Files (x86)\AWR\AWRDE\10\MWOffice.exe" \
   raw_native_types \
   rename("AddPort", "AddPort2") \
   exclude("IMeasurement")
```

The `#import` directive instructs the Visual C++ compiler to automatically generate header and implementation files for the COM library. You can find this in the output directory with a name that matches the library, in this case `mwoffice.tlh` and `mwoffice.tli`. Since this is in the precompiled header file, the header is automatically included in all of your source files.

## Use the COM Library

Our final step is to use the COM library in C++. We want to do the equivalent of what we previously executed in C#. The equivalent code in C++ is:

```
int _tmain(int argc, _TCHAR* argv[])
{
    ::CoInitialize(NULL);
    MWOffice::Application* mwoApp;
    HRESULT hRes = ::CoCreateInstance(__uuidof(MWOffice::Application), NULL, CLSCTX_ALL, __uuidof(MWOffice::IMWOffice), (void**)&mwoApp);
    if (SUCCEEDED(hRes))
    {
    }
    ::CoUninitialize();
    return 0;
}
```

There is nothing special here, except for how did I get the names of the objects? Where did `MWOffice::Application` and `MWOffice::IMWOffice` come from? They came from the C# project I created earlier. In Visual Studio, open up the `Object Browser` and select the `Application` class. From there, we can see the base type is` IMWOffice`.

[](https://s3-us-west-2.amazonaws.com/ficksworkshop/media/blog/how-to-connect-to-awr-design-environment-component-api-from-c/object_browser.png)

At this point, there's only one thing left to do. Compile and run.