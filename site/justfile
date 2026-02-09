set windows-shell := ["powershell.exe", "-c"]

default: install build test

install:
    bundle install

build:
    bundle exec jekyll build

test:
    bundle exec rake checkhtml
    export LANG=en_US.UTF-8 && export LANGUAGE=en_US:en && export LC_ALL=en_US.UTF-8 && bundle exec rake spellcheck

run:
    bundle exec jekyll serve

