# Description

This is a work-in-progress Rest API for an e-commerce app. The technologies being used are Dajngo and Dajngo Rest Framework with a PostgreSQL database.
The API capabilities allow CRUD operations on the endpoints for users, products, categories, inventory, reviews and more.

The goal is to create a modern platform where users can buy and sell products, therefore, the API allows:
 - Product Listing
 - Shopping Cart
 - Order Management
 - Products Reviews
 - Products Questions (not implemented yet)
 - Messages Between Sellers And Customers (not implemented yet)

The platform is intended to be structured in a multi-tier architecture deployed on AWS.
<br><br>


# Installation

### Clone The Repository

```console
git clone https://github.com/Eadwulf/e-commerce-api
```

### Change Directory

```console
cd e-commerce-api
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

The project uses a PostgreSQL database. Configured as follows

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
<br>


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
    💡 Be aware that <em>django-environ</em> is required. Such dependency should be installed
    by running <em>pipenv install</em>
</aside>
<br>

### Apply the migrations

```python
python manage.py migrate
```
<br>

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