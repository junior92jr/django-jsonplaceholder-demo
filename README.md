# Rest Service for Placeholder Fake Api

This Rest Service creates a simple REST API to interact with the `Fake API in JSONPlaceholder - Free Fake REST API`. Additionally, it includes a way to constantly synchronize the data.

## Tech Stacks
* Python 3.11
* Django 4.2
* Django Rest Framework 3.14
* PostgrSQL 16.2
* JWT Authentication
* Docker/Docker-Componse

## Set up the project

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
and starting a PSQL console.

```bash
$ docker-compose exec web-db psql -U postgres

psql (16.2)
Type "help" for help.

postgres=#
```

### Check Django container is running

We can confirm the Django container was properly created by running the `check` command.

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

We need to run the Django command `sync_fake_api_data`. You can run it as many times as you wish.

Internally, it is creating the data if it does not exist; otherwise, It will insert objects not present in the database and search for differences with existing objects to update.

```bash
$ docker-compose exec web python manage.py sync_fake_api_data
```

We synchronize the objects in the database with `BULK CREATE` and `BULK UPDATE` Transactions to ensure ACIDity, handle rollbacks and avoiding multiple writes to the database.

### Setting Cronjobs (Optional Step)
Internally, we Also set up some Cron Jobs that will run the synchronizing tasks at 00:00 and 01:00 CET every day.

```bash
    '0 0 * * *',
    'posts.tasks.sync_posts.synchronize_posts_task',
    '>> /cron/django_cron.log 2>&1'

    '0 1 * * *',
    'posts.tasks.sync_comments.synchronize_comments_task',
    '>> /cron/django_cron.log 2>&1'
```

You only need to indicate that you want to add them to the container.

```bash
$ docker-compose exec web python manage.py crontab add
```

It is possible to check the logs for the Crontabs.

```bash
$ docker-compose exec web cat /cron/django_cron.log
```

## Authentication
The Project uses a Bearer Token Authentication based on JWT. All endpoints are protected, So you need to generate an `access` token. It will last for 5 minutes. You can refresh that access token for 1 day only.

It is possible to modify the values in the `settings.py` file.

### Generate Access Token

```bash
Request
    curl --location 'http://localhost:8000/api/token/' \
    --header 'Content-Type: application/json' \
    --data '{
        "username": "admin",
        "password": "admin_pass"
    }'
```

```bash
Response
    {
        "refresh": "eyJh ... eM3JZIg",
        "access": "eyJhb ... EqmQpdY"
    }
```

### Refresh Token

```bash
Request
    curl --location 'http://localhost:8000/api/token/refresh/' \
    --header 'Content-Type: application/json' \
    --data '{
        "refresh": "eyJh ... eM3JZIg"

    }'
```

```bash
Response
    {
        "access": "iuKnj ... SolSwRZ"
    }
```

### Bearer Token in the Header
For all endpoints, you will need to use `Authorization` Header.

```bash
    curl --location 'http://localhost:8000/api/v1/posts/' \
    --header 'Authorization: Bearer eyJhb...EqmQpdY'
```

## Api Usage
All items contain `created_at` and `updated_at` values. It indicates the date when it was created and updated.

```bash
    "created_at": "2024-03-15T12:06:19.947938+01:00",
    "updated_at": "2024-03-15T12:54:41.036391+01:00"
```

For `Posts` and `Comments`, when using successfully the methods `PUT`, `PATCH` and `DELETE`. All changes will be synchronized with the `Fake API` results when running `sync_fake_api_data` or the cronjobs are executed (if those last ones were added).

```bash
$ docker-compose exec web python manage.py sync_fake_api_data
```

### Posts
The `external_id` is the `id` from the Source where it was imported; if it is, `null` means it was created internally.

The `user_id` will contain `99999942` if it was created internally as well.

#### List All
```bash
GET /api/v1/posts/
GET /api/v1/posts/?external_id=1
GET /api/v1/posts/?external_id=1&user_id=1
GET /api/v1/posts/?user_id=1
```
#### Retrieve by ID
```bash
GET /api/v1/posts/1/
```

#### Create
```bash
PUT /api/v1/posts/1/
```

```bash
Body
    {
        "title": "editing title",
        "body": "editing body",
    }
```

#### Full/Partial Update
```bash
PATCH /api/v1/posts/1/
```

```bash
Body
    {
        "body": "partial edit",
    }
```

```bash
POST /api/v1/posts/
```

```bash
Body
    {
        "title": "new post title",
        "body": "new post body "
    }
```

#### Delete
```bash
DELETE /api/v1/posts/1/
```

### Comments

The `post` is the `pk` in the database for the existing Post.

#### List All

```bash
GET /api/v1/comments/
GET /api/v1/comments/?external_id=1
GET /api/v1/comments/?post=4
GET /api/v1/comments/?external_id=1&post=4
```

#### Retrieve by ID
```bash
GET /api/v1/comments/1/
```

#### Create
```bash
POST /api/v1/comments/
```

```bash
Body
    {
        "post": 2,
        "name": "new comment name",
        "email": "newemail@mail.com",
        "body": "new comment body"
    }
```

#### Full/Partial Update
```bash
PUT /api/v1/comments/1/
```

```bash
Body
    {
        "post": 5,
        "name": "edited new comment name",
        "email": "editednewemail@mail.com",
        "body": "edited new comment body"
    }
```

```bash
PATCH /api/v1/comments/1/
```

```bash
Body
    {
        "name": "edited new comment name",
        "email": "editednewemail@mail.com",
    }
```

#### Delete
```bash
DELETE /api/v1/comments/1/
```

## Running Test
For running the test, we use Django testing tools and a testing database in memory database.

```bash
docker-compose exec web python manage.py test --settings=manager.test_settings
```
