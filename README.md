# Electronic Program Guide - Async Workers
An async program that takes requests to fetch TV guides, spins up async celery workers to do the job.


## How to run this:
### Requirements
- [Docker](https://www.docker.com/)

### App setup
- Create `.env` file following the example in `.env.example`
- Add the domain you are hosting the application on to the ALLOWED_HOSTS in the .env file.
- Spin up the docker containers.
- Create a folder in the root directory called `temp`. We will use this to clone the siteini.pack in the next step.
- First you need to hit the endpoint that updates the `siteini.pack` folder. You can look at the swagger docs to find the endpoint. Currently the endpoint for that is `update-site-pack` end it accepts a get request.

### Local setup/Staging/Development
- run the containers `docker compose up`

### Production Setup
- Create `.env` file following the example in `.env.example`
- Assumes that there is a `postgres` database outside of docker that the app can connect to.
-  run the containers `docker compose -f docker-compose.yml -f docker-compose.prod.yml up`
- We can running the container in a detached state using the command.
`docker compose -f docker-compose.yml -f docker-compose.prod.yml up --detach`


### Migrations
- Once you have container up and running, you need to get into the `web` service and run migrations.
- You can do that like this:
- Access the container using the command `docker compose exec web bash` where web is the name of the service we defined in the docker compose file.
- Run the migrations using the command `python manage.py migrate`

### API Documentation
- With the server running go to the url `http://127.0.0.1:8000/swagger-ui`.

## Docker
This application makes use of docker to spin up several services to get the job done.
### Docker services
#### Web
This service runs Django. 

#### Postgres
A postgres for the Django application. Running postgres `postgres:15.3`.
this is defined in `docker-compose.override.yml`.

#### Redis
We are using the [redis server](https://redis.io/docs/about/) as a message broker for Celery. [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) is the task queue we are using.

#### celery_worker_one
We have each celery worker running as a container, this is because of how WebGrab the scrapper we are using runs. Otherwise one celery worker container and making using of concurrency would have worked. To add a new worker copy one of the existing celery_workers. 

## How to:
1. how to access a service running on the host machine from within a container?
    -  we set up extra_hosts on the web_service. So from within the `web` service we can access the host like this.
    ```
     curl http://host.docker.internal:8080
    ```
    to access a service running on port `8080` on the host machine.
2. See the docker containers that are running.
    ```
     docker ps
    ```
3. Get the logs of specific container
   ```
   docker logs -f <name_of_container>
   ```
   you can get the name of the container from the previous step. 
4. Check the status of the celery workers.
    - First get into the web container. `docker compose exec web bash`
    - Check the workers. `celery -A web_grab inspect active` where `web_grab` is the name of the project. See celery [docs](https://docs.celeryq.dev/en/stable/userguide/monitoring.html)
### Tutorial on how to use Django and Celery.
- [Real python tutorial](https://realpython.com/asynchronous-tasks-with-django-and-celery/#handle-workloads-asynchronously-with-celery)

