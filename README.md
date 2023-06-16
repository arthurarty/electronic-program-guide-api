# Electronic Program Guide - Async Workers
An async program that takes requests to fetch TV guides, spins up async celery workers to do the job.


## How to run this:
#### Requirements
- Docker


### Local setup/Staging/Development
- Create `.env` file following the example in `.env.example`
- run the containers `docker compose up`

### Production Setup
- Assumes that there is a `postgres` database outside of docker that the app can connect to.
-  run the containers `docker compose -f docker-compose.yml -f docker-compose.prod.yml up`

### Migrations
- Once you have container up and running, you need to get into the `web` service and run migrations.
- You can do that like this:
- Access the container using the command `docker compose exec web bash` where web is the name of the service we defined in the docker compose file.
- Run the migrations using the command `python manage.py migrate`

## Docker
This application makes use of docker to spin up several services to get the job done.
### Docker services
#### Web
This service runs Django. 

#### Postgres
A postgres for the Django application. Running postgres `postgres:15.3`.
this is defined in `docker-compose.override.yml`.

#### Redis
We are using the (redis server)[https://redis.io/docs/about/] as a message broker for Celery. (Celery)[https://docs.celeryq.dev/en/stable/getting-started/introduction.html] is the task queue we are using.

#### celery_worker_one
We have each celery worker running as a container, this is because of how WebGrab the scrapper we are using runs. Otherwise one celery worker container and making using of concurrency would have worked. To add a new worker copy one of the existing celery_workers. 

### Tutorial on how to use Django and Celery.
- https://realpython.com/asynchronous-tasks-with-django-and-celery/#handle-workloads-asynchronously-with-celery
