build *ARGS:
    just site/build {{ARGS}}

test:
    just site/test
    just infra/test

deploy:
    just infra/deploy
