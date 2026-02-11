build *ARGS:
    just site/build {{ARGS}}

deploy:
    just infra/deploy
