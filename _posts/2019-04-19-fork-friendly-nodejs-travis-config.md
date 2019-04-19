---
layout: post
title: Fork-Friendly Node.js Travis CI Configuration
date: 2019-04-19
---

I've been recently contributing to [CloudSploit's scans](https://github.com/cloudsploit/scans)
and gotten a few changes merged in. Their current usage pattern is to use Git to obtain the
code an run it on their infrastructure (I don't actually know this is true, so I'm making assumptions
based on the available docs and some other things i can find).

To make things nicer, I've been setting up Travis CI builds for automated tests (since there were no
tests in the repository). My next step was to publish a package to NPM. However, I see my work as a
fork - I'm not the authority nor do I want to be. But I do want things to work for me.

This means I wanted to publish a scoped package from my fork. And I want our builds to be able to
depend on my scoped package, while still allowing cloudSploit to publish a package, if they so choose.
Without a little magic, I would have to maintain different build scripts and `package.json` file.

The default case for NPM and Travis CI don't play nicely in terms of allowing forks, but with a little
effort, you can make it possible, and this post shows how.

Requirements:

* NPM credentials cannot be baked into `.travis.yml` (since forks will be different)
* You need to be able to change the package name in `package.json` so that forks can publish their
  own scoped package.
  
You can satify these all with Travis CI. Thus, my YML file looks like the following (your package would
need to replace "cloudsploit" with the right package name.

```
language: node_js
node_js:
  - "stable"

# Deployment of cloudsploit is setup to work nicely both for the master repo
# any forks. That is, a fork can also publish to NPM to a custom scope. To do
# this, you need to do the following in the Travis CI settings for your account
#
# 1. Add an environment variable with the name NPM_SCOPE and a value like
#
#    @yourname\/
#
#  Note the @ symbol and slash are all important and shoud not be changed.
#
# 2. Add an environment variable with the name NPM_EMAIL and the email
#    associated with your NPM account.
#
# 3. Add an environment variable with the name NPM_API_KEY containing your
#    npm token.
#
# Finally, publishing only happens on tagged commits - so if you want to
# publish to your scoped package, then you need to create a tag (and of course
# publish it with git push --tags).
#
# Handling version numbers is ugly now and you'll still have to update
# package.json. Sorry, but I haven't yet figured out a better way. :(
before_deploy:
  # You need to create a variable in your Travis CI settings to provide the
  # npm package scope. This allows forks to publish under their own name.
  - sed -i 's#"cloudsploit"#"'$NPM_SCOPE'cloudsploit"#g' package.json
deploy:
  # We modify package.json to change the package name automatically, so
  # don't to cleanup otherwise that would revert the package name change.
  skip_cleanup: true
  provider: npm
  email: $NPM_EMAIL
  api_key: $NPM_API_KEY
  on:
    # Only try to publish when a tag was pushed.
    tags: true
 ```

Then in your Travis CI build, define the environment variables that we'll use. For my
CloudSploit fork, they are:

![](static/img/blog/2019-04-19-travis-ci-npm-scoped-package.png)

By making things configurable, you are able to publish both a default package and
scoped packages easily, the difference being applied only through some environment
variables.

The result can be seen as two packages on NPM: [cloudsploit](https://www.npmjs.com/package/cloudsploit)
and [@garretfick/cloudsploit](https://www.npmjs.com/package/@garretfick/cloudsploit).

