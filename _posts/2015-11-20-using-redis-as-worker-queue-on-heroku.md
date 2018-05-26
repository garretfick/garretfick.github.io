---
layout: post
title: Using Redis as Django Worker Queue on Heroku
date: 2015-11-20
---

[Heroku documentation recommends using Redis Queue](https://devcenter.heroku.com/articles/python-rq) to setup worker tasks. But for me, that document was pretty incomplete for how to setup Redis Queue for a production Django application. This guide will show you how you can setup Redis Queue to schedule regular worker tasks for a Django application running on Heroku.

What do I mean by "schedule regular worker tasks"? I mean run some code on a regular basis, for example every day email a report of users over the last day. Or, for example, every 12 hours automatically delete some cached data from your database. This guide is also useful if you want to schedule tasks in response to a particular action, but that isn't my focus.

## Install Redis Server For Local Testing

First, you'll need to setup Redis Server for local testing. Run the following to install Redis Server

```
sudo apt-get install redis-server
```

## Create the Worker App

Our goal is to be able to run tasks in our Django app, and the scheduled tasks are probably going to use your existing Django apps and models. If you want to do that, then you want to let Django set everything up the way it expects. The best way to do that is with custom Django management commands. For that, create two commands:

* `manage.py worker`: execute the actual tasks on worker dynos
* `manage.py scheduler`: schedule tasks using [Heroku Scheduler](https://elements.heroku.com/addons/scheduler)

Depending on your project layout, create a new `worker` app with the following files (`__init__.py` not shown):

```
worker
    management
        commands
            scheduler.py
            worker.py
    connection.py
```

The content of these files is similar to the Heroku documentation - the biggest difference is I've split out the connection information into a separate module to better share it.

`connection.py` contains the common connection information for connecting to Redis

```
import os
import redis
import urlparse
from rq import Worker, Queue, Connection
listen = ['high', 'default', 'low']
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
url = urlparse.urlparse(redis_url)
conn = redis.StrictRedis(host=url.hostname, port=url.port, password=url.password)
```

`worker.py` processes the items in the queue

```
from rq import Worker, Queue, Connection
from django.core.management.base import BaseCommand
from apps.worker.connection import conn, listen
class Command(BaseCommand):
    def handle(self, *args, **options):
        with Connection(conn):
            worker = Worker(map(Queue, listen))
            worker.work()
```

`scheduler.py` adds items to the queue

```
from rq import  Queue
from apps.worker.connection import conn
from django.core.management.base import BaseCommand
class Command(BaseCommand):
    def handle(self, *args, **options):
        q = Queue(connection=conn)
        result = q.enqueue(YOUR_FUNCTION_HERE)
```

## Test Locally

If everthing is setup correctly, you can start the worker and then schedule tasks.

Run the following to start the worker listener:

```
$python manage.py worker
```

Then in another terminal, run the following to schedule some tasks:

```
$python manage.py scheduler
```

If your tasks produce any outut, you will see them in the worker's terminal.

## Provision Heroku Add-on

In order to be able to use [RedisToGo](https://elements.heroku.com/addons/redistogo) on Heroku, you need to povision the addon. Run the following to provision the addon:

```
heroku addons:create redistogo:nano
```

With that in place, you should be able to run both the worker and scheduler on Heroku on-off dynos:

Execute the following to run the worker:

```
heroku run python manage.py worker
```

Execute the following to run the scheduler:

```
heroku run python manage.py scheduler
```

*Note* You can only run one one-off dyno so you won't be able to see them interact using one-off dynos.

## Add to the Procfile and Scale the Worker

The worker process will run in the background, so you need to define it in Procfile and then scale the worker. Add the following to your Procfile

```
worker: python ./manage.py worker
```

After deploying the code, scale up a worker process

```
heroku ps:scale worker=1
```

## Schedule the Scheduler

The final piece is to regularly add tasks the to queue (that's what the scheduler does). An easy way do to that is via the Heroku Scheduler Add-on

```
heroku addons:create scheduler:standard
```

Then head over to the [Scheduler configuration](https://scheduler.heroku.com/dashboard) page on Heroku and set the scheduler to run periodically:

Finally, sit back and watch your application start taking care of itself automatically.