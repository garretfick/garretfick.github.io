---
layout: post
title: Setup and Run Django+Heroku Locally on Windows
date: 2015-08-19
---

This is part 2 of a 4 part series on how to setup Django locally on Windows and deploy to Heroku.

1. Introduction
2. Setup and Run Django+Heroku Locally on Windows (this page)
3. Change from SQLite to PostgreSQL
4. Split Windows and Linux Configurations

This page covers how to get everything installed and running locally on Windows, including running locally via Heroku.

## Heroku Toolbelt

Setting things up is mostly an exercise in executing a series of commands at the command line, and it is much easier to run the commands via the Bash Command Prompt. The Heroku Toolbelt includes the Git Bash Command Prompt, so install that first.

[Download Heroku Toolbelt](https://toolbelt.herokuapp.com/) then install.

## Python and Virtualenv

Django is written in Python (you already knew that didn't you), so install Python.

[Download Python 3.4.3](https://www.python.org/downloads/release/python-343/) then install. This release already includes the necessary setuptools and pip packages.

*Note* This guide will work with other version of Python which you can find on [python.org](http://python.org/), but I'm assuming this version to keep the instructions simple. If you use a different version, make sure to use the correct components of psycopg2-windows.

A virtualenv allows installing Python packages locally to a particular project (instead of globally across a computer), and thus allows different projects to use different versions of Python packages.

Open a Git Bash command prompt (included with Heroku Toolbelt) and execute the following to install the virtualenv Python package:

```
/c/Python34/Scripts/pip install virtualenv
You are using pip version 6.0.8, however version 7.1.0 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
Collecting virtualenv
Downloading virtualenv-13.1.0-py2.py3-none-any.whl (1.7MB) 100%
|################################| 1.7MB 121kB/s
Installing collected packages: virtualenv
Successfully installed virtualenv-13.1.0
```

## Create the Project's Virtualenv

In the command prompt, change directories to directory that will store the project, then execute the following (speedydjango is the name of our project):

```
mkdir speedydjango && cd speedydjango
```

Then execute the following to create a virtualenv in the project directory:

```
/c/Python34/Scripts/virtualenv venv
Using base prefix 'C:\\Python34'
New python executable in venv\Scripts\python.exe
Installing setuptools, pip, wheel...done.
```

Finally, execute the following to activate the virtualenv so that installing Python packages installs them into the virtualenv:

```
source venv/Scripts/activate
(venv)
```

## Install Django and Create the Project

Next, install Django into the isolated project space. There are two ways do this:

* Directly specify Django at the command line
* Indirectly specify Django via a requirements file

Heroku specifies dependencies using a requirements file so we should do the same.

In the project directory, create a new file named `requirements.txt` with the following content:

```
Django==1.8
```

Then execute the following to download and install Django:

```
pip install -r requirements.txt --allow-all-external
```

If everything was successful, the Django framework was installed to `venv\Lib\site-packages\django`. This is still only the framework, not a Django project. Execute the following to create a Django project:

*Note* Don't forget the period at the end to create the project into the current directory

```
django-admin.py startproject speedydjango .
```

Finally, execute the following to verify that everything is setup correctly:

```
manage.py --version
1.8
```

## Create `Procfile` and Run

Heroku uses a [`Procfile`](https://devcenter.heroku.com/articles/procfile) to define and execute the web server processes. In the project directory, create a new file named `Procfile` (capital P, no extension) with the following content:

```
web: python manage.py runserver 0.0.0.0:$PORT --noreload
```

*Note* At the time of writing, there seems to be an issue with forego that doesn't replace $PORT. If you get this error, replace $PORT with a specific port number. However, you must use the variable $PORT when deploying to Heroku.

This `Procfile` declares one `web` process type which runs the standard startup script for Django.

After all this work, test it out by starting the web server the Heroku way:

```
heroku local
```

Then in your browser, navigate to `localhost:3456` and you should see the following:

Next change from SQLite to PostgreSQL.