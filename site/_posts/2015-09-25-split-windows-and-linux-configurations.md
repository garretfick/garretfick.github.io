---
layout: post
title: Split Windows and Linux Configuration
date: 2015-09-25
---

This is part 4 of a 4 part series on how to setup Django locally on Windows and deploy to Heroku.

1. Introduction
2. Setup and Run Django+Heroku Locally on Windows
3. Change Django from SQLite to PostgreSQL
4. Split Configuration for Windows and Linux (this page)
5. 
You may recall from the first page that setting up Django locally on Windows and deploying to Heroku has a problem. If the application uses PostgreSQL, then the configuration between Windows and Linux cannot be the same.

This final part describes how to setup the configuration (requirements) so that Windows and Linux have different requirements.

## Two Requirements

The easiest way to specify different requirements is to have two `requirements.txt` files: one for local development and one for production. [Heroku's Python buildpack](https://github.com/heroku/heroku-buildpack-python) uses `requirements.txt`, so unless you want to change the buildpack, the easiest way to set things up is:

* `requirements.txt`: production (or staging)
* `devel-requirements.txt`: local development


Create a copy of `requirements.txt` and name it `devel-requirements.txt`. This is the existing Windows requirements for location development. Then open `requirements.txt` and replace

```
-e git+https://github.com/nwcell/psycopg2-windows.git@win64-py34#egg=psycopg2
```

with

```
psycopg2==2.6
```

## Commit to Git

Before adding and committing to Git, there are a few things that should not be committed to Git.

Since you cannot directly create a file name in Windows starting with a period, execute the following to create the `.gitignore` file:

```sh
touch .gitignore
```

Then either open the file add the following:

```sh
*.pyc venv
```

or paste the full contents of [GitHub's awesome standard `.gitignore`](https://github.com/github/gitignore/blob/master/Python.gitignore), adding the line:

```sh
venv
```

Then execute the following to add the files to Git:

```
git add . && git commit -m "Ficksworkshop is awesome! :)"
```


*Note* At this point, you should store your code in a remote repository. Personally, I use [BitBucket](http://bitbucket.org/) because it allows free private repositories - but there are lots of other great alternatives.

## Push to Heroku

The final step is to create a [Heroku](http://www.heroku.com/) application and push to Heroku. First login to Heroku:

```
heroku login
```

Then, in the same folder as the application, execute the follow to create a new Heroku application:

```
heroku apps:create APPNAME
```

*Note* You must rename the application to something unique.

Finally, push your code to Heroku:

```
git push heroku master
```

## Migrate the Database

Since this is the first time using this database for Django, the tables don't match what Django expects. Just as when running locally, the database needs to be migrated, but this time, using the heroku CLI to run the migration on the server.

```
heroku run python manage.py migrate
```

## View the Running Application

If everything worked, the application is now running on Heroku. Point your browser to `APPNAME.herokuapp.com` to see it running.