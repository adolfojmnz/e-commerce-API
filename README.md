# Description

This is a work-in-progress Rest API for an e-commerce app. The technologies being used are Dajngo and Dajngo Rest Framework with a PostgreSQL database.
The API capabilities allow CRUD operations on the endpoints for users, products, categories, inventory, reviews and more.

The goal is to create a modern platform where users can buy and sell products, therefore, the API allows:
 - Product Listing
 - Shopping Cart
 - Order Management
 - Products Reviews
 - Q&A In Products (not implemented yet)
 - Private Messages Between Sellers And Customers (not implemented yet)

The platform is intended to be structured in a multi-tier architecture deployed on AWS.

The presentation layer (front-end) es being developed as Netx.js App. <br>
Repo: [E-Commerce-Next.js](https://github.com/Eadwulf/e-commerce-nextjs)
<br><br>


# Installation

### Clone The Repository

```console
git clone https://github.com/Eadwulf/e-commerce-API
```

### Change Directory

```console
cd e-commerce-API
```

### Install The Dependencies And Activate The Virtual Environment

```console
pipenv install && pipenv shell
```

<aside>
    💡 Make sure to install <a href="https://pypi.org/project/pipenv/">pipenv</a> on your system
</aside>
<br><br>


# Database Setup

This project requires a PosgreSQL database, but alternatively, you could use a Sqlite3 database.

## Setup With Sqlite3 Database

### Change The Database Configurations In The `config/settings.py`

```python
# config/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

If you decided to set up the Sqile3 database, skip the next section and jump to
the **Environment Variables** section
<br>


## Setup With PostgreSQL Database

### The Database Settings Are Set As Follows

```python
# config/settings.py

DATABASES = {
    'default': {
	'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
    },
}
```

<aside>
    💡 If you do not have an existing database and user to use with these settings, follow the
    instructions below and create new ones.
</aside>
<br>

### Enter The PostgreSQL Prompt

```sql
psql -U postgres -d postgres
```

### Create The Database

```sql
CREATE DATABASE <database_name>;
```

### Create The User

```sql
CREATE USER <username> WITH ENCRYPTED PASSWORD '<password>';
```

### Modifying Connection Parameters

```sql
ALTER ROLE <database_user> SET client_encoding TO 'utf8';
ALTER ROLE <database_user> SET default_transaction_isolation TO 'read committed';
ALTER ROLE <database_user> SET timezone TO 'UTC';
```

### Grant Permissions To The User

```sql
 GRANT ALL PRIVILEGES ON DATABASE <database_name> TO <username>;
```

### Exit The Prompt

```sql
\q
```

# Environment Variables

### Create The Environment Variables File **(.env)**

In the root directory *(e-commerce-API/)*, create the **.env** file and add to it the following

```python
DEBUG=<boolean_value>
SECRET_KEY=<your_django_api_key>
DATABASE_NAME=<your_database_name>
DATABASE_HOST=<your_database_host>
DATABASE_PORT=<your_database_port>
DATABASE_USER=<your_database_user>
DATABASE_PASSWORD=<your_database_password>
```
<aside>
    💡 Note:
    <ul>
      <li>
        <p>
          <em>django-environ</em> is required to load the environment variables in the `config/settings.py` file.
          Such dependency should be installed by running <em>pipenv install</em>
        </p>
     </li>
     <li>
       <p>
          If you are setting a Sqlite3 database instead of a PostgreSQL, don't include the environment variables for the
          database as they are not required when working with Sqlite3.
       </p>
     </li>
</aside>
<br>

### Generate The SECRET_KEY

To run the project, you will need to set a secret key to the `SECRET_KEY` environment variable.
Create one by running

```console
$ python manage.py shell
```

Once in the Django Shell

```python
>>> from django.core.management.utils import get_random_secret_key

>>> get_random_secret_key()
```

It will output a key such as

```python
'30p0cw(#l0z7%2ao7t)%!%h+(v3y+6(#=vbj8x&-snly(#(pu#'
```

<aside>
  💡 Add the key to the corresponding environment variable.
    Don't forget to remove the single quotation marks (') at the beginning and the end of the key
</aside>
<br>

# Migrations

Once the database is set up as well as the environment variables, you can proceed to apply the migrations

```python
python manage.py migrate
```

# Tests

So far, a total of 49 tests are available. Such tests ensure that the models and the API endpoints work as expected.
<br>

### Run the tests
```console
python manage.py test
```

It should return an output such as

```console
Found 49 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.................................................
----------------------------------------------------------------------
Ran 49 tests in 16.937s

OK
Destroying test database for alias 'default'...
```

# Endpoints Documentation

## Introduction

This documentation describes the usage and functionality of the endpoints exposed by the API. It provides information on the available resources, request, and response formats.

- **Request Format**: application/json
- **Response Format**: application/json

# Users

- **Description**:
- **URL**: localhost:8000/api/users
- **HTTP Method**: GET, POST

### GET Request

- **Description**: Retrieves the list of active users
- **************************Status Code:************************** 200 OK
- **Example**:

    Request:

    ```bash
    curl -X GET localhost:8000/api/users \
       -H "Content-Type: application/json"
    ```

    Response:

    ```json
    [
    	{
    		"id": {userId},
    		"email": "bob.fellow@localhost.com",
    		"username": "bob",
    		"first_name": "Bob",
    		"last_name": "Fellow",
    		"about": "Short about sample",
    		"avatar_url": "/media/avatars/bob_01.jpg",
    		"birthdate": "1980-04-11",
    		"is_active": true,
    		"last_login": "2023-04-11T12:40:52Z",
    		"date_joined": "2023-04-11T12:39:46Z"
    	},
    	{
    		"id": {userId},
    		"email": "ana.fellow@localhost.com",
    		"username": "ana",
    		"first_name": "Ana",
    		"last_name": "Fellow",
    		"about": "Short about sample",
    		"avatar_url": "/media/avatars/ana_01.jpg",
    		"birthdate": "1999-12-31",
    		"is_active": true,
    		"last_login": null,
    		"date_joined": "2023-04-26T11:04:21.103660Z"
    	}
    ]
    ```


### POST Request

- **Description**: Creates a new user
- ********Status Code:******** 201 CREATED, 400 Bad Request
- **Example**:

    Request:

    ```bash
    curl -X POST localhost:8000/api/users \
       -H "Content-Type: application/json" \
    	 -d '{"username": "pete", "password": "pa/^#ss63wd", "birthdate": "1980-04-11"}'
    ```

    Response:

    ```json
    {
    	"id": {userId},
    	"email": "",
    	"username": "pete",
    	"first_name": "",
    	"last_name": "",
    	"about": "",
    	"avatar_url": "",
    	"birthdate": "1980-04-11",
    	"is_active": true,
    	"last_login": "",
    	"date_joined": "2023-04-11T12:39:46Z"
    }
    ```


# Users/{userId}

- **Description**:
- **URL**: localhost:8000/api/users/{userId}
- **HTTP Method**: GET, PATCH, DELETE

### GET Request

- **Description**: Retrieves the list of active users
- **************************Status Code:************************** 200 OK
- **Example**:

    Request:

    ```bash
    curl -X GET localhost:8000/api/users/{userId} \
       -H "Content-Type: application/json"
    ```

    Response:

    ```json
    {
    	"id": {userId},
    	"email": "ana.fellow@localhost.com",
    	"username": "ana",
    	"first_name": "Ana",
    	"last_name": "Fellow",
    	"about": "Short about sample",
    	"avatar_url": "/media/avatars/ana_01.jpg",
    	"birthdate": "1999-12-31",
    	"is_active": true,
    	"last_login": null,
    	"date_joined": "2023-04-26T11:04:21.103660Z"
    }
    ```


### PATCH Request

- **Description**: Updates an existing user
- ********Status Code:******** 200 OK, 400 Bad Request
- **Example**:

    Request:

    ```bash
    curl -X PATCH localhost:8000/api/users/{userId} \
       -H "Content-Type: application/json" \
    	 -d '{"email": "pete.fellow@localhost.com", "first_name": "Pete", "last_name": "Fellow"}'
    ```

    Response:

    ```json
    {
    	"id": {userId},
    	"email": "pete.fellow@localhost.com",
    	"username": "pete",
    	"first_name": "Pete",
    	"last_name": "Fellow",
    	"about": "",
    	"avatar_url": "",
    	"birthdate": "1980-04-11",
    	"is_active": true,
    	"last_login": "",
    	"date_joined": "2023-04-11T12:39:46Z"
    }
    ```


### DELETE Request

- **Description**: Sets an existing user as inactive (is_active = False)
- ********Status Code:******** 204 NO CONTENT
- **Example**:

    Request:

    ```bash
    curl -X DELETE localhost:8000/api/users/{userId} \
       -H "Content-Type: application/json"
    ```

    Response:

    ```json
    []
    ```


# Users/current

- **Description**: This endpoint inherits the functionalities of the `api/users/{userId}` endpoint.

    Interfacing with this endpoint is just as it is with the one it inherits, being the only difference the URL used to make the requests.

- **URL**: localhost:8000/api/users/**************current**************
- **HTTP Method**: GET, PATCH, DELETE
- **Example**:

    Request:

    ```bash
    curl -X GET localhost:8000/api/users/current \
       -H "Content-Type: application/json"
    ```