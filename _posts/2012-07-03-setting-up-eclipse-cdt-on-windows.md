---
layout: post
title: Setting up Eclipse CDT on Windows
date: 2012-07-03
---

I wanted to compile my own version of [libxml2](http://www.xmlsoft.org/) on Windows using [GCC](http://gcc.gnu.org/) and the [Eclipse CDT](http://www.eclipse.org/cdt/) environment. (You can also use the Visual Studio project included with libxml2, but I needed to compile with GCC.) You can follow the steps below to setup an environment the Eclipse CDT environment and build libxml2.

## Install Java

Eclipse is built on Java, and so it needs the Java RTE.

1. [Download Java](http://java.com/en/download/manual.jsp)
2. Run the installer to install

I downloaded the 64-bit version because I have a 64-bit version of Windows.

## Install Eclipse CDT

Eclipse releases a number of packages for different development scenarios. The easiest way to get Eclipse for C/C++ development is to install Eclipse CDT (essentially Eclipse with C Development Tools).

1. [Download Eclipse CDT](http://www.eclipse.org/cdt/)
2. Unzip the contents and copy to `C:\Program Files`.

If you installed the same as I did, you should see the program `C:\Program Files\Eclipse\eclipse.exe`

## Install Tools and Compiler

Eclipse CDT doesn't come with a compiler or the tools needed to build the software. There are a few options here, and I elected to install [MinGW](http://www.mingw.org/).

1. [Download the MinGW installer](http://sourceforge.net/projects/mingw/files/Installer/mingw-get-inst/)
2. Run the installer to install.

During installation, make sure you select everything you need. I selected everything except the Objective C, Fortran and Ada compilers.

Once you've installed MinGW, you have to add it to your path so that Eclipse can find it.

1. Browse through `Control Panel > System and Security > System > Change Settings`
2. On the `Advanced` tab, click `Environment variables`
3. If the user PATH environment variable exists append the following including the semicolon:

    ```
    ;C:\MinGW\bin;C:\MinGW\msys\1.0\bin
    ```

    otherwise, create a new PATH environment variable, and set the value to

    ```
    C:\MinGW\bin;C:\MinGW\msys\1.0\bin
    ```

At this point, everything is setup for use with any C/C++ project.

## Create the Eclipse Project

My objective was to compile libxml2, so the following steps relate specifically to compiling libxml2. You can either drop off here, or continue to understand how to setup the Eclipse project.

1. [Download the latest libxml2](ftp://xmlsoft.org/libxml2/)
2. Extract the contents to `C:\work\libxml2`. If you extracted as I suggested, you should see the file `C:\work\libxml2\README`
3. Start Eclipse. Set the workspace path to `C:\work`
4. In Eclipse, select File > New > C++ Project, and set the following settings, then click Next and Finish
    1. Set the project name to libxml2. The location should show as `C:\work\libxml2` and you should see a warning that a project already exists at that location
    2. Set the project type to `GNU Autotools > Empty Project`
5. Set the compiler path using the following steps
    1. Select the libxml2 project. Select `Project > Properties`
    2. Browse to `C/C++ General > Paths and Symbols`
    3. Select `GNU C++`

## Build libxml2

Hopefully everything above worked. Now you're ready to build.

1.Select `Project > Build All`

This will take a while, especially for the configure script, but when it's done, you should have a built DLL.