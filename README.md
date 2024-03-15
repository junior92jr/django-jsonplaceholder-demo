# Rest Service for Placeholder Fake Api

This Rest Service creates a simple REST API to interact with the `Fake API in JSONPlaceholder - Free Fake REST API`. Additionally it includes a way to synchronize the data constantly.

## Tech Stacks
* Python 3.11
* Django 4.2
* Django Rest Framework 3.14
* PostgrSQL 16.2
* JWT Authentication
* Docker/Docker-Componse

## Set up the Project

### Clone the repository

To clone the repository by SHH

```bash
$ git clone git@github.com:junior92jr/posts_service.git
```

To clone the repository by HTTPS

```bash
$ git clone https://github.com/junior92jr/posts_service.git
```

## Build the API image

To build, test and run this API we'll be using `docker-compose`. As such, the first step
is to build the images defined in the `docker-compose.yml` file.

```bash
$ cd posts_service/
```

```bash
$ docker-compose build
```

```bash
$ docker-compose up
```

This will build two images:

- `django-app` image with the Django App.
- `postgres-db` image with Postgres database.

### Create Enviroment Variables

You will find a file called `.env_example`, rename it for `.env`

### Run the Containers
 
To run the containers previously built, execute the following:
 
```bash
$ docker-compose up -d
```

To make sure the app is running correctly open [http://localhost:8000](http://localhost:8000).

### Check database is running

We can confirm that the database was properly created by accessing the database container
and starting a psql console.

```bash
$ docker-compose exec web-db psql -U postgres

psql (16.2)
Type "help" for help.

postgres=#
```

### Check Django container is running

We can confirm that django container was properly created by running the check command.

```bash
$ docker-compose exec web python manage.py check

System check identified no issues (0 silenced).
```

### Import Placeholder API data
We need to run the django command `sync_fake_api_data`.

```bash
$ docker-compose exec web python manage.py sync_fake_api_data
```

### Create Admin User
We would need the `User` to be able to authenticate and access the Rest Service Endpoints.

```bash
$ docker-compose exec web python manage.py createsuperuser

Username (leave blank to use 'root'): admin
Email address: admin@mail.com
Password: admin_pass
Password (again): admin_pass

Superuser created successfully.
```

You will be asked for `username`, `email` and `password`.


## Synchronizing data from the Placeholder API to our Database

We need to run the django command `sync_fake_api_data`. You can run it many times as you wish.

Internally it is creating the data if it not exists otherwise It will Insert or Update for objects not present in the database and look for differences with existing objects.

```bash
$ docker-compose exec web python manage.py sync_fake_api_data
```

Internally we Also set up some Cron Jobs that will run the synchronizing tasks at 00:00, 01:00 CET time every day.

```bash
    '0 0 * * *',
    'posts.tasks.sync_posts.synchronize_posts_task',
    '>> /cron/django_cron.log 2>&1'

    '0 1 * * *',
    'posts.tasks.sync_comments.synchronize_comments_task',
    '>> /cron/django_cron.log 2>&1'
```

It is possible to check the logs for the Crontabs

```bash
$ docker-compose exec web cat /cron/django_cron.log
```

## Authentication
The Project uses a Bearer Token Authentication based on JWT. All endpoints are protected So you need to generate an `access` token. It will last for 5 minutes. You can refresh that access token for 1 day only.

### Generate Access Token

Request

```bash
    curl --location 'http://localhost:8000/api/token/' \
    --header 'Content-Type: application/json' \
    --data '{
        "username": "admin",
        "password": "admin_pass"
    }'
```

Response

```bash
    {
        "refresh": "eyJh ... eM3JZIg",
        "access": "eyJhb ... EqmQpdY"
    }
```

### Refresh Token

Request

```bash
    curl --location 'http://localhost:8000/api/token/refresh/' \
    --header 'Content-Type: application/json' \
    --data '{
        "refresh": "eyJh ... eM3JZIg"

    }'
```

Response

```bash
    {
        "access": "iuKnj ... SolSwRZ"
    }
```

### Bearer Token in the Header
For all endpoints you will need to use `Authorization` Header.

```bash
    curl --location 'http://localhost:8000/api/v1/posts/' \
    --header 'Authorization: Bearer eyJhb...EqmQpdY'
```
