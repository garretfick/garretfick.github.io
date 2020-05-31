---
layout: post
title: Installing GCC on Mac
date: 2015-11-20
---

Suppose you want to use the latest and greatest version of GCC on the Mac because you want to use features in [C++11](http://en.wikipedia.org/wiki/C%2B%2B11) that are not yet available in XCode. There are probably a few ways to do this, but one way is via [MacPorts](http://www.macports.org/) which provides precompiled binaries for tons of packages.

You can follow the following steps to install GCC 4.7 via MacPorts. Others versions (including GCC 4.8) follow a pretty similar procedure.

1. Browse to the [MacPorts website](http://www.macports.org/install.php). Download the DMG image for your operating system
2. Install the package
3. Open up a terminal `Applications > Utilities > Terminal`
4. Make sure that you have the latest version by running the self update via the terminal command

    ```
    sudo port selfupdate
    ```

5. Install GCC via the terminal command

    ```
    sudo port install gcc47
    ```

    Now sit back and wait while MacPorts does its thing. One MacPorts is done, the next thing is to compile a simple program. Running gcc or g++ at the command line invokes the compiler installed with XCode. The new executables are installed to
    
    `/opt/local/bin/gcc-mp-4.7`
    
    and
    
    `/opt/local/bin/g++-mp-4.7`

6. Depending on your build environment, you may want to access GCC by running gcc or g++ at the command line. Because the MacPorts are installed to another location, you either need to either specify the full path, or set the compiler to use on your system. For the second option, you can use MacPorts to select the default compiler. First, identify which versions are installed on your system.

    ```
    port select --list gcc
    ```

    In my case, this returns

    ```
    Available versions for gcc:
       gcc42
       llvm-gcc42
       mp-gcc47
       none (active)
    ```

    To select GCC 4.7, run the command

    ```
    sudo port select --set gcc mp-gcc47
    Password:
    Selecting 'mp-gcc47' for 'gcc' succeeded. 'mp-gcc47' is now active.
    ```