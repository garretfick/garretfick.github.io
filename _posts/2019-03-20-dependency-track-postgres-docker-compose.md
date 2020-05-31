---
layout: post
title: Dependency Track with Postgres and Docker Compose
date: 2019-03-20
---

I've recently been investigating [Dependency Track](https://dependencytrack.org/) for
understanding risks in third-party software that we use. To make things easy, I've
been running locally via docker.

One lesson is that you need a real database such as Postgres. The compose file below
will get you started with Dependency Track connected to Postgres running in another
container.

```yml
version: '3.1'
services:
  dtrack:
    environment:
    - ALPINE_DATABASE_MODE=external
    - ALPINE_DATABASE_URL=jdbc:postgresql://db:5432/dtrack
    - ALPINE_DATABASE_DRIVER=org.postgresql.Driver
    - ALPINE_DATABASE_DRIVER_PATH=/extlib/postgresql-42.2.5.jar
    - ALPINE_DATABASE_USERNAME=dtrack
    - ALPINE_DATABASE_PASSWORD=password
    image: 'owasp/dependency-track'
    ports:
    - '8090:8080'
    volumes:
    - './data:/data'
    restart: always
    depends_on:
    - db
  db:
    environment:
    - POSTGRES_PASSWORD=password
    - POSTGRES_USER=dtrack
    - POSTGRES_DB=dtrack
    image: 'postgres:10'
    restart: always
    ports:
    - '5432:5432'
    volumes:
      - ./db:/var/lib/postgresql
```

Once things are up an running, you can login to the UI from [http://localhost:8090/](). You can then login with the default credentials listed in the [Dependency Track documentation](https://docs.dependencytrack.org/getting-started/initial-startup/).

This isn't sufficient for a production system (you probably want LDAP, SSH, etc). But this is enough for local evaluation.
