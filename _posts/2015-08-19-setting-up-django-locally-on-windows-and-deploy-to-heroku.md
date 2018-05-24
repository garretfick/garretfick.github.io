---
layout: post
title: Setting up Django Locally on Windows and Deploy to Heroku
date: 2015-08-19
---

Setting up [Django 1.8](https://www.djangoproject.com/) with [PostgreSQL](http://www.postgresql.org/) to run on [Heroku](http://heroku.com/) - that's straightforward. Just follow the official Heroku documentation [Getting Started with Django on Heroku](https://devcenter.heroku.com/articles/getting-started-with-django). But what if you want or need to do development locally on Windows? Then this is the guide for you.

This guide will show you how to setup the following stack:

* Python 3.4.3
* Django 1.8
* PostgreSQL 9.3.4

and how you can develop on Windows and deploy to Heroku Linux.

![](https://s3-us-west-2.amazonaws.com/ficksworkshop/media/blog/setting-up-django-locally-on-windows-and-deploy-to-heroku/stack_logos.png)

For this guide, I'll assume you are starting from scratch - as in you just installed a new copy of Windows. I'll also try to explain some of the why so when this guide becomes out of date, you can hopefully figure out how to handle new version numbers.

If you just want to final code, [grab it from Bitbucket](https://bitbucket.org/garretfick/win-lin-django).

Why Develop on Windows

Before we get into the details, I want to first talk about why.

Getting Django to run on Windows is harder than on Linux. You often have to find reliable pre-compiled packages. Your development environment will not exactly match your production environment so you may run into issues that are unique to one environment or the other. Remember that even if you boot to Windows, you can still installl Linux in a virtual machine, such as [VirtualBox](https://virtualbox.org/), and develop on Linux.

Then why am I explaining how to setup a Windows environment? I sometimes spend long periods of time disconnected from power and running in a virtual machine drains the battery faster. I still maintain a Linux virtual machine for primary development - the Windows environment is secondary.

Think twice before going down the path of Windows as your primary development environment. But if you still want to, I'll tell you how.

## How

There are quite a few steps to get things running, so I've split this guide into several parts.

1. Introduction (this page)
2. Setup and Run Django+Heroku Locally on Windows
3. Change from SQLite to PostgreSQL
4. Split Windows and Linux Configurations