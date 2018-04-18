# Falcon Case

## Requirements
The task is to implement a data processing pipeline in the cloud. Set up a running environment aligned with the technologies mentioned below:

- :heavy_check_mark: A Readme file containing information you deem useful for someone getting to know your code and want to try the system out.
- :heavy_check_mark: Develop the application in Python 3.
- :heavy_check_mark: A REST endpoint is taking a dummy JSON input, and the server puts the REST payload on Redis or another tool you think is well suited for the task.
- :heavy_check_mark: A Consumer is running in the application, taking the freshly received message and persists it in a database of your choice.
- :heavy_check_mark: A REST endpoint is implemented for retrieving all the messages persisted in JSON format from the database.
- :heavy_check_mark: The message should also be pushed through Websockets for listening browser clients at the time the message was received on the REST endpoint
- :heavy_check_mark: A simple HTML page is implemented to show the real time message delivery
- :heavy_check_mark: Please setup a github repository to host the code and share it with your final note for review

## We're looking for that:

- :heavy_check_mark: All tasks are solved in the solution
- :heavy_check_mark: The application has a solid commit history
- :heavy_check_mark: The application is built with scalability and maintainability in mind
- :heavy_check_mark: The application is built for testability, demonstrated by actual tests
- :heavy_check_mark: Your solution reflects a sense of quality you would be confident in releasing to production
- :heavy_check_mark: Documentation is applied to code / repository describing intent and purpose, as well as complicated / non obvious choices in the implementation

## Architecture
The architecture pattern chosen is the microservice pattern. 
The application is run inside a docker container that is loosely coupled to other docker containers in which additional functionality is provided.
Specifically, the web service itself is run in it's own container, run by nginx and served using uwsgi and python3.6. 
In addition to the web service, celery, is also used to provide asynchronous task handling.
Flower is also utilised to provide real-time monitoring of celery.
The web service is dependent on separate containers: A postgresql container for providing database persistance. A redis container for providing cache functionality. An adminer container for providing administrative access to the database through a control panel.
The reason that this pattern was chosen is the ease of which it allows for:
- Portability and Deployability: Any platform where docker is supported, the application can be run.
- Scalability: You can always add more celery workers to handle message persistance.

To give you a more complete picture of what docker images are used for the application, they are as follows:

- `tiangolo/uwsgi-nginx-flask:python3.6` - python3.6 is the development language that the API was implemented in, and the image provides a web server through `nginx` and an application server through `uwsgi`.
- `redis:alpine` - redis is used as an in-memory cache for the data requested over the API.
- `postgres:alpine` - postgres is used to persist the JSON objects on a database.
- `mher/flower` - flower used for providing real-time monitoring.
- `adminer` - adminer is used to provide an administrative overview of the postgres database.

## How To Use
The application can be run by using `docker-compose`.

To get started, ensure that you have docker installed, and execute the following commands:

- `docker-compose build`
- `docker-compose up`

This will create the docker images, and the different docker containers that are then started to host the API. The url for the server is `http://127.0.0.1/api` which contains Swagger documentation for the endpoints that were implemented. The actual endpoint for the API is `http://127.0.0.1/endpoint/` The url for the flower page where real time updates can be seen is `127.0.0.1:5555`

For testing, it is important that the database is clean so it should be run before anything else is done, the following command will execute the testing:

- `python run_tests.py`
