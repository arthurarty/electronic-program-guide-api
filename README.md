# webgrab_container
Containerising web grab


## How to run this:
#### Requirements
- Docker


### Optional step (only needed if you see odd import issues)
- install the package so that subpackages can import from each other. To do this run `python setup.py install`

### Local setup/Staging/Development
- run the containers `docker compose up`

### Production Setup
- Assumes that there is a `postgres` database outside of docker that the app can connect to.
-  run the containers `docker compose -f docker-compose.yml -f docker-compose.prod.yml up`

### Docs on how to accomplish something like this:
- https://realpython.com/asynchronous-tasks-with-django-and-celery/#handle-workloads-asynchronously-with-celery
