---
layout: post
title: Using Terraform to Build Heroku/S3 Site
date: 2017-05-07
---

I have been playing around with [Terraform](http://www.terraform.io), and decided to try to use terraform to build a staging environment for this site. (In fact, I actually already had a
staging environment - this was just for my own interest).

My site consists of a simple [Heroku](https://heroku.com) hosted application with static resources
stored in [AWS S3](https://aws.amazon.com/s3/). My first step was to define my application's architecture in the terrafrom configuration file.

For my purposes, I wanted to start with a pretty simple definition. If you follow the [Terraform Getting Started](https://www.terraform.io/intro/getting-started/install.html) guide, you will end up with three files:

1. `terraform.tf` containing your infrastracture definition
2. `variables.tf` containing variable definitions for your infrastructure definition
3. `terraform.tfvars` containing the variable values, such as API keys

Let's begin with `variables.tf` - this will give a good idea of what we need in order to build the application.

```
# Authentication for the AWS provider - we use this access
# key in order to be able to create a new AWS user and the S3
# bucket that the application needs.
variable "aws_access_key_id" {}
variable "aws_access_secret_key" {}
variable "aws_region" {
  default = "us-west-1"
}

# Authentication for the Heroku provider - we use this access
# key in order to be able to create a new Heroku application
# and provision the addon
variable "heroku_email" {}
variable "heroku_api_key" {}

# Application environment - usually something like 'staging' or 'prod'
# We use this to label items and generate names
variable "app_environment" {}

# Heroku app settings
# This is the name of the Heroku application that we will create
# This needs to be unique (no to accounts can have the same name)
variable "heroku_app_name" {}
variable "heroku_app_region" {
  default = "us"
}
# The application needs to provision a database. This the plan level
# for the basic Heroku Postgress database
variable "heroku_db_plan" {
  default = "heroku-postgresql:hobby-basic"
}

# Defines whether our application is a debug version
# The default should be false
variable "app_debug" {
  default = "false"
}
# On Heroku, define how the application logs. We use the
# errorlog so that Heroku can collect the logs from the
# application. This setting is specific to the Laravel-based
# application we are running.
variable "app_log" {
  default = "errorlog"
}

# A unique key for the application. This setting is specific
# to the Laravel-based application we are running.
variable "app_key" {}

# The URL for the application. This setting is specific
# to the Laravel-based application we are running.
variable "app_url" {
  default = "ficksworkshp.com"
}

# Defines which Laravel backend to use for saving files.
# We are using S3. This setting is specific
# to the Laravel-based application we are running.
variable "filesystems_default" {
  default = "s3"
}

# AWS and S3 settings - these define the details of the S3 bucket that we will create
# The credentials to access the bucket are created automatically by terraform
variable "filesystem_s3_user_name" {}
variable "filesystems_s3_bucket" {}
variable "filesystems_s3_region" {
  default = "us-west-2"
}
variable "resource_tag_name" {}
```

With that in mind, let's define the application infrastructure. That happens in `terraform.tf`.

```
# This terraform configuration generates a Heroku PHP application
# using the Heroku postgress database addon and creates an AWS S3
# bucket to host static files for the application.
# The site is sufficiently simple that this configuation is
# contained in a single file (except for the variables)

# We need the Heroku provider in order to create the Heroku application
provider "heroku" {
  email = "${var.heroku_email}"
  api_key = "${var.heroku_api_key}"
}

# We need the AWS provider in order to create the S3 bucket
provider "aws" {
  access_key = "${var.aws_access_key_id}"
  secret_key = "${var.aws_access_secret_key}"
  region     = "${var.aws_region}"
}

# Creates the IAM key for write access to the S3 bucket
# We need to create the IAM users, give that user an access
# key, and finally give that user write access to the bucket
# with a policy
resource "aws_iam_user" "iam_user_s3_rw" {
  name = "${var.filesystem_s3_user_name}"
  # You cannot tag a user, but you can give them a path
  # to help identify the context of the user
  path = "/${var.resource_tag_name}/"
  
}

# Creates the API key for the user
resource "aws_iam_access_key" "s3_rw" {
  user    = "${aws_iam_user.iam_user_s3_rw.name}"
}

# Restricts the user to only the S3 bucket they should
# have access to
resource "aws_iam_user_policy" "policy_s3_rw" {
  # We concatenate the user name with the policy to ensure that
  # the policy name is unique, but still recognizable
  name = "${aws_iam_user.iam_user_s3_rw.name}-policy"
  user = "${aws_iam_user.iam_user_s3_rw.name}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:*"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:s3::::${var.filesystems_s3_bucket}"
    }
  ]
}
EOF
}

resource "aws_s3_bucket" "aws_bucket_static" {
  bucket = "${var.filesystems_s3_bucket}"
  acl    = "private"

  tags {
    Name        = "${var.resource_tag_name}"
    Environment = "${var.app_environment}"
  }

  acl    = "public-read"

  cors_rule {
    allowed_origins = ["*"]
    allowed_methods = ["GET"]
    max_age_seconds = 3000
    allowed_headers = ["*"]
  }
}

# Creates the primary Heroku application.
resource "heroku_app" "default" {
  name = "${var.heroku_app_name}"
  region = "${var.heroku_app_region}"

  # We do need a URL for the database, but we don't
  # need to create it because provisioning the
  # addon automatically created this config var
  config_vars = {
      APP_DEBUG = "${var.app_debug}"
      APP_KEY = "${var.app_key}"
      APP_LOG = "${var.app_log}"
      APP_URL = "${var.app_url}"
      FILESYSTEMS_DEFAULT = "${var.filesystems_default}"
      FILESYSTEMS_S3_KEY = "${aws_iam_access_key.s3_rw.id}"
      FILESYSTEMS_S3_BUCKET = "${var.filesystems_s3_bucket}"
      FILESYSTEMS_S3_REGION = "${var.filesystems_s3_region}"
      FILESYSTEMS_S3_SECRET = "${aws_iam_access_key.s3_rw.secret}"
  }

  buildpacks = [
      "heroku/php"
  ]
}

# Create the Heroku Postgress addon for the application
resource "heroku_addon" "database" {
  app  = "${heroku_app.default.name}"
  plan = "${var.heroku_db_plan}"
}
```

The final piece is `terraform.tfvars`. The specific values will depend on your particular site, but the file looks like the following:

```
app_environment = "VALUE"
filesystem_s3_user_name = 
aws_access_key_id = 
aws_access_secret_key = 
filesystems_s3_bucket = 
heroku_api_key =
heroku_app_name = 
heroku_email = 
app_key = 
```

Now save those to your main directory. You can then execute `terraform plan` and `terraform apply` to build your infrastructure. Pretty cool!