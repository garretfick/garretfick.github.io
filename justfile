set windows-shell := ["powershell.exe", "-c"]

run:
    bundle exec jekyll serve

test:
    bundle exec rake checkhtml
    export LANG=en_US.UTF-8 && export LANGUAGE=en_US:en && export LC_ALL=en_US.UTF-8 && bundle exec rake spellcheck