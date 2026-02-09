---
layout: post
title: Setting up a October CMS environment with Vagrant and Heroku
date: 2017-03-20
---

OctoberCMS is an interesting CMS platform build on Laravel. There is a great official tutorial on how to setup OctoberCMS
with a Vagrant box using the quick install approach.

That approach is great if you will use OctoberCMS's project management tools to update, install plugins, themes, etc.
But if you want to do any custom work, including install a composer package, you are out of luck. The quick install doesn't
include composer.json, so there is no way forward.

Alternatively, you can setup OctoberCMS via command line, which will give you a standard PHP/composer project, but there is
no tutorial on how do to that, but the steps are pretty straightforward.

This tutorial will show you how to setup OctoberCMS as a normal PHP/composer project inside a Vagrant box. Later tutorials
cover important security considerations that I think OctoberCMS does horribly wrong, how to deploy the project to Heroku
(my favorite PaaS solution) and finally additional configuration you will need in order for your application to work
with Heroku's ephemeral storage and across multiple instances.

## Get the Vagrant Box (Scotch Box)

Open a terminal window. Execute the following to create directory
for your project and then clone the scotch-box repository into
the directory.

```sh
mkdir octobercms && cd octobercms
git clone https://github.com/scotch-io/scotch-box .
```

## Customize the Vagrant Box

The default Scotch Box is a good start, but we want to make a few changes
so it works well for OctoberCMS and Heroku.

### Change the mapped `public` directory

First, change the default directory so that we can install OctoberCMS in
the root directory. This allows Heroku to easily identify our application
as a PHP application.

Open `Vagrantfile` in a text editor. Replace

```
config.vm.synced_folder ".", "/var/www", :mount_options => ["dmode=777", "fmode=666"]
```

with

```
config.vm.synced_folder ".", "/var/www/public", :mount_options => ["dmode=777", "fmode=666"]
```

### Configure PHP 7.1

OctoberCMS works well with PHP 7.x and older versions of PHP will
soon be deprecated. It is good idea to start a new project with an
environment that will be supported in the future. Scotch Box only has
PHP 5.6, but we can configure it to install PHP 7.1.

Open `Vagrantfile` in a text editor. After the line `config.vm.hostname = "scotchbox"`, add the following (maintaining the same 4-space indentation):

```
    config.vm.provision :shell, path: "bootstrap.sh"
```

Then get `bootstrap.sh` download from https://gist.github.com/garretfick/7b27eaf88dbe4762e994b875e9de23b6 and save it
to the root directory, for example:

```
curl -O  https://gist.githubusercontent.com/garretfick/7b27eaf88dbe4762e994b875e9de23b6/raw/d10e736a3a6d0ddfe9b684c6ea26432cfbd32f8d/bootstrap.sh
```

## Install OctoberCMS

Now that the Vagrant box is in a good state, we can proceed with
installing OctoberCMS.

### Start the Vagrant box

We will install OctoberCMS within the Vagrant box. In the terminal window, execute the following to start and connect to the virtual
machine.

```sh
vagrant up && vagrant ssh
```

### Update composer

Composer, how we will get and install OctoberCMS gets regular updates. If desired, update composer so you have a recent version.

```sh
sudo /usr/local/bin/composer self-update
```

### Create an OctoberCMS project

We want to install OctoberCMS using composer. However, composer will only
install into an empty directory which is incompatible with how Heroku expects to find your project. So, we will create the the project in a
temporary directory, then move the files into the desired location.

```sh
cd /var/www/public
composer create-project october/october temp dev-master --prefer-dist
```

At the end of the installation, composer will prompt you if you want to keep the project history. Choose `Y`

```
Do you want to remove the existing VCS (.git, .svn..) history? [Y,n]? Y
```

Then move the files to the root project directory.

```
mv temp/{*,.*} ./ && rmdir temp
```

_The `{*,.*}` syntax to make sure to copy the hidden files._

### Validate your setup

At this point, you should be able to see the OctoberCMS site running
via your browser.

On your host machine, enter the IP address of your site (or URL if
you are using the hostupdater Vagrant plugin). You should see the
OctoberCMS welcome page.

### Create a git repository

Deploying to Heroku requires a git repository (and you should be
tracking your source code changes in source control anyway).

In a terminal window, execute the following to create a git repository
for your project and stage your initial commit.

```
git init && git add .
```

Most projects have files that should not be committed to the repository.

Open `.gitignore` in a text editor. Add the following

```
# Ignore the vagrant box virtual machine files
/.vagrant

# Ignore Laravel/OctoberCMS logs and cache
storage/logs/
storage/framework/
```

Also, remove the item `composer.lock` (which should be tracked and is required
for deploying on Heroku).

The `.gitignore` above ignores a few files that we don't want excluded,
so force them to be added to the repository.

```
git add -f storage/**/.gitignore storage/framework/services.json
```

Finally, commit your change.

```
git commit -m "Initial commit of website code"
```

**Tip**: If you are running git within the Scotch Box, you will need to tell git a little about yourself before you can commit your first change.

```
git config --global user.email "your.email@example.com"
git config --global user.name "Your Name"
```

**Tip**: Although outside the scope of this tutorial, this is a good time to setup a remote repository and push your code there.

## Customize the OctoberCMS installation

Although we have a working OctoberCMS installation, isn't quite
compatible with our Vagrant box nor Heroku.

### Disable OctoberCMS updates

Since we are using composer, we don't want to use OctoberCMS's update
mechanism.

Open `config/cms.php` in a text editor. Find `disableCoreUpdates` and
set it's value to `true` as below:

```
'disableCoreUpdates' => true,
```

### Setup database connection and admin User

OctoberCMS comes with an installer to help setup a DB connection
and default user based on the MySQL instance that is part of the
Scotch Box. We'll use it to start things, but then customize
it further so it works with Heroku and is secure in the next step.

In the terminal window, execute the following

```
php artisan october:install
```

When prompted, input the following:

1. Database type: 0 (MySQL)
2. MySQL Host: `localhost`
3. MySQL Port: 3306
4. Database Name: `scotchbox`
5. MySQL Login: root
6. MySQL Password: root
7. First Name: Admin
8. Last Name: Person
8. Email Address: your.email@example.com
9. Admin Login: admin
10. Admin Password: admin
11. Application URL: `http://localhost`
12. Configure advanced options: no

The installer should complete successfully.

### Externalize environment configuration

The default configuration of OctoberCMS encourages you to put the database
passwords and other sensitive information in the configuration files. This
won't work if you want to have different passwords for your local development
(vagrant box) and production (Heroku) environments. It is also very insecure
because the configuration files are checked into your git repository.

In the terminal window, execute the following to externalize your passwords
to a `.env` file which we have already ignored with the `.gitignore` file.

```
php artisan october:env
```

### Set good production defaults

As a good practice, your default configuration settings should be set to
be safe for your production environment. That way, if you forget to configure
your production environment, your configuration is what makes sense for
production.

Open `config/app.php` in a text editor.  Find `log` and
set it's default value to `errorlog` as below:

```
'log' => env('APP_LOG', 'errorlog'),
```

### Test out the backend

At this point, you should be able to see the OctoberCMS backend running via your browser.

On your host machine, enter the IP address of your site followed by `/backend` (or URL if you are using the hostupdater Vagrant plugin). You should be able to login
with the credentials you input above.

### Commit your customization to Git

Assuming all of the above works, you are at a good checkpoint before we do some
final customization for Heroku.

In the terminal window, execute the following to stage and then commit your changes

```
git add .
git commit -m "Externalize configuration settings"
```

**Tip** You will not commit the `.env` file because this file contains your
sensitive and instance specific information.

## Setup Heroku

Our goal was to setup the application so that you can deploy it to a PaaS provider
such as Heroku. So far, we have a site that runs locally in a virtual machine. Our
next step is to get things working on Heroku.

I'll assume you have already installed the Heroku CLI. If you haven't, get that first.

### Create a new Heroku application

Next, in the terminal window, execute the following to create a new Heroku
application.

```
heroku apps:create your-app-name
```

### Setup Heroku to use PHP 7.1

Since we are using PHP 7.1 on our virtual machine, we should also configure
Heroku to use PHP 7.1.

Open `composer.json` in a text editor. Find `php` in the `require` section and change it's value to `>=7.0` as below:

```
"php": ">=7.0",
```

### Create a `composer.lock` file

The `composer.lock` file tells composer precisely which version of packages to
install for your application. The default OctoberCMS create project script does
not include this file, but it is a requirement for Heroku's PHP support. However,
it is easy to generate it from your installation.

In the terminal window, execute the following to update and generate the lock file.

```
composer update
```

### Deploy to Heroku

Deploying to Heroku is as easy as pushing to git. First, however, we need to commit
our changes.

```
git add . && git commit -m "Setup Heroku support"
```

then push your changes to Heroku

```
git push heroku
```

and finally view your site running on Heroku

```
heroku open
```

When the page loads, it should look strange - as though none of the JavaScript and CSS files were loaded. We will solve this and
other issues in the next article.