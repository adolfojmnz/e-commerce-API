# Description

### A RESTFull API for an e-commerce app.

This project has been developed with Python using Django and Django Rest Framework.
It is powered by a PosgreSQL database.

So far, it has a CI workflow defined with GitHub Actions which sets up and tests the
code committed to this GitHub repo, subsequently, it builds and pushes
a Docker Image to Docker Hub.

This RESTFull API features Jason Web Token authentication and several endpoints with
defined levels of authorization based on the requesting user's role.

The project's endpoints allow to perform CRUD operations on multiple database models,
such as:
 - Products
 - Inventory
 - Categories
 - Shopping Cart and Shopping Cart Items
 - Orders and Order Items
 - Reviews

The project is being structured as a three tiers architecture with:
 - Data Tier: PostgreSQL database
 - Presentation Tier: Netx.JS Application
 - Backend Tier: Django Application (This RESTFull API)


The presentation tier (front-end) can be found in the
[E-Commerce-Next.js](https://github.com/Eadwulf/e-commerce-nextjs) repo.
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
    'NAME': env('POSTGRES_DB'),
    'HOST': env('POSTGRES_HOST'),
    'PORT': env('POSTGRES_PORT'),
    'USER': env('POSTGRES_USER'),
    'PASSWORD': env('POSTGRES_PASSWORD'),
    },
}
```

<aside>
    💡 If you do not have an existing database and user to use with these settings, follow the
    instructions below and create new ones.
</aside>
<br>

### Enter Into The PostgreSQL Prompt

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

### Modifying User's Parameters

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
POSTGRES_DB=<your_database_name>
POSTGRES_HOST=<your_database_host>
POSTGRES_PORT=<your_database_port>
POSTGRES_USER=<your_database_user>
POSTGRES_PASSWORD=<your_database_password>
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

To run the project, you will need to set a Django secret key to the `SECRET_KEY` environment variable.
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

Once the database has been set up as well as the environment variables, you can apply the migrations

```python
python manage.py migrate
```

# Tests

The project includes more than eighty (80) tests that ensure its correct functioning. The tests
cover constraints, business logic, permission, and authorization.

All the endpoints and their allowed HTTP methods are tested.

### Run the tests
```console
python manage.py test
```

Example output

```console
Found 88 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
........................................................................................
----------------------------------------------------------------------
Ran 88 tests in 54.432s

OK
Destroying test database for alias 'default'...
```

# Entity Relationship Diagram

![Database ERD](./ERD.png)

# API Documentation

## Introduction

This documentation describes the usage and functionality of the endpoints exposed by the API. It provides information on the available resources, request, and response formats.

- **Request Format**: application/json
- **Response Format**: application/json

## JWT Endpoints

### Token

- **Description**: Obtain JWT token pair (access and refresh tokens) for a registered user.
- **URL**: localhost:8000/api/token/
- **HTTP Method**: POST
- **Example**:

    Request:

    ```bash
    curl -X POST localhost:8000/api/token/ \
       -H "Content-Type: application/json" \
       -d '{"username": "bob", "password": "pa/^#ss63wd"}'
    ```

    Response:

    ```json
    {
      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4NDU5NzY4OCwiaWF0IjoxNjg0NTExMjg4LCJqdGkiOiI5NjIxOGU3NDgzYTg0YzM0ODc5YjZmYWQyYWI3NzljYSIsInVzZXJfaWQiOjF9.ka4BJ94bCRUzcJNfxVSabr0cApdUm0haXmPVFg81dKA",
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg0NTk3Njg4LCJpYXQiOjE2ODQ1MTEyODgsImp0aSI6ImI2ZmYxNjExZTEwYTQxNjY5OWZmOTc3YzBmM2U2ZTUzIiwidXNlcl9pZCI6MX0.oWe8pwBdfv8s8mWZl81k_swle1mVdOSOJEGZYJtY8nQ"
    }
    ```


### Token/refresh

- **Description**:  Obtain a new access token by using an active refresh token.
- **URL**: localhost:8000/api/token/refresh/
- **HTTP Method**: POST
- **Example**:

    Request:

    ```bash
    curl -X POST localhost:8000/api/token/refresh/ \
       -H "Content-Type: application/json" \
       -d '{"username": "bob", "password": "pa/^#ss63wd"}'
    ```

    Response:

    ```json
    {
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg0NTk3Njg4LCJpYXQiOjE2ODQ1MTEyODgsImp0aSI6ImI2ZmYxNjExZTEwYTQxNjY5OWZmOTc3YzBmM2U2ZTUzIiwidXNlcl9pZCI6MX0.oWe8pwBdfv8s8mWZl81k_swle1mVdOSOJEGZYJtY8nQ"
    }
    ```


## Users

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

- **Description**: Creates a new user with the given data.
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

- **URL**: localhost:8000/api/users/{userId}
- **HTTP Method**: GET, PATCH, DELETE

### GET Request

- **Description**: Retrieves the user for userId
- **************************Status Code:************************** 200 OK, 404 NOT FOUND
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
       -H "Authorization: Bearer {access_token}" \
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
- ********Status Code:******** 204 NO CONTENT, 404 NOT FOUND
- **Example**:

    Request:

    ```bash
    curl -X DELETE localhost:8000/api/users/{userId} \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}"
    ```

    Response:

    ```json
    {"message": "The user has been set as inactive."}
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
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}"
    ```


## Products

- **Description**:  Allows the retrieval of the product list as well as the creation of new ones.
- **URL**: localhost:8000/api/products
- **HTTP Methods**: GET, POST
- **Example**:

    GET Request:

    ```bash
    curl -X GET localhost:8000/api/products \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}"
    ```

    GET Response (status code 200):

    ```json
    [
      {
        "id": {productId},
        "name": "Cobalt (Walnut/Blue)",
        "brand": "Holzkern",
        "image_url": {imageURL},
        "description": "Cobalt is a naturally occurring element that can be found in the ground, the air and also in the bodies of living creatures. Its bonding properties have been used for the coloration of glass and ceramics since antiquity.",
        "specifications": {
          "color": "Walnut/Gray",
          "movement": "quartz",
          "release date": "2023-04-10",
          "case material": "metal-wood",
          "diameter (mm)": 42,
          "is waterproof": true,
          "bracelet material": "metal-wood",
          "has date indicator": false,
          "has chronograph features": false
        },
        "price": "499.00",
        "vendor": {userId},
        "category": {categoryId},
        "available": true,
        "quantity": 7,
        "rating": null,
        "total_reviews": 0
    	},
    	{
          "id": {productId},
          "name": "ASUS TUF Gaming A16 Advantage Edition (2023)",
          "brand": "ASUS",
          "image_url": {imageURL},
          "description": "Jump right into the action with the TUF Gaming A16 Advantage™ Edition. Stream and multitask with ease thanks to the latest AMD Ryzen™ 9 7940HS CPU and up to 32GB of blisteringly fast 4800MHz DDR5 RAM on Windows 11. Leverage the full gaming performance of up to a AMD Radeon™ RX 7700S GPU with AMD Smart Access Graphics. When your game library gets full, an empty M.2 NVMe SSD slot makes upgrading storage capacity a breeze.",
          "specifications": {
            "OS": "Windows 11",
            "CPU": "Ryzen 9 7940HS",
            "GPU": "Raedon RX 7700S",
            "RAM": "32GB 4800MHz DDR5 Dual-Channel",
            "Disk": "2TB PCIe 4.0 2x SSD",
            "Refresh Rate": "240Hz QHD, 165Hz FHD",
            "Charging Type": "Type-C  50% in 30 mins",
            "Military Grade": "MIL-STD 810H Passed",
            "Battery Capacity": "90Wh",
            "Battery duration": "Up to 13.6 Hours of Video Playback",
            "Screen-to-body Ratio": "90%"
          },
          "price": "1699.99",
          "vendor": {userId},
          "category": {categoryId},
          "available": true,
          "quantity": 6,
          "rating": 5.0,
          "total_reviews": 4
    	},
    ]

    ```

    <aside>
    💡 Thanks to the `specifications` field, specific features can be added to different types of products without having to define them as specific fields in the product table.

    </aside>

    POST Request:

    ```bash
    curl -X POST localhost:8000/api/products \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}" \
       -d '{"name": "Headset Razer Kraken Ultimate", "brand": "Razer", "description": "Headset description", "specifications": null, "price": "129.99", "category": {categoryId}, "available": true, "quantity": 10}'
    ```

    <aside>
    💡 This post request creates an entry in the inventory_item for the created product and its quantity. In addition, the user that makes the request will be selected as the vendor of the product.

    </aside>

    POST Response (status code 201):

    ```json
    {
      "id": {productId},
      "name": "Headset Razer Kraken Ultimate",
      "brand": "Razer",
      "image_url": "",
      "description": "Headset description",
      "specifications": null,
      "price": "129.99",
      "vendor": {userId},
      "category": {categoryId},
      "available": true,
      "quantity": 10,
      "rating": null,
      "total_reviews": 0
    }
    ```


## Products/{productId}

- **Description**:  Allows the retrieval, edition, and deletion of a product.
- **HTTP Methods**: GET, PATCH, DELETE
- **URL**: localhost:8000/api/products/{productId}
- **********************Permissions**********************: PATCH and DELETE requests on a product can only be made by their vendors.
- **Example**:

    GET Request:

    ```bash
    curl -X GET localhost:8000/api/products/{productId} \
       -H "Content-Type: application/json" \
    ```

    GET Response (status code 200):

    ```json
    {
      "id": {productId},
      "name": "Cobalt (Walnut/Blue)",
      "brand": "Holzkern",
      "image_url": {imageURL},
      "description": "Cobalt is a naturally occurring element that can be found in the ground, the air and also in the bodies of living creatures. Its bonding properties have been used for the coloration of glass and ceramics since antiquity.",
      "specifications": {
        "color": "Walnut/Gray",
        "movement": "quartz",
        "release date": "2023-04-10",
        "case material": "metal-wood",
        "diameter (mm)": 42,
        "is waterproof": true,
        "bracelet material": "metal-wood",
        "has date indicator": false,
        "has chronograph features": false
      },
      "price": "499.00",
      "vendor": {userId},
      "category": {categoryId},
      "available": true,
      "quantity": 7,
      "rating": null,
      "total_reviews": 0
    }
    ```

    PATCH Request:

    ```bash
    curl -X PATCH localhost:8000/api/products/{productId} \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}" \
       -d '{"image_url": {imageURL}, "quantity": 100}'
    ```

    PATCH Response (status code 200):

    ```json
    {
      "id": {productId},
      "name": "Headset Razer Kraken Ultimate",
      "brand": "Razer",
      "image_url": {imageURL},
      "description": "Headset description",
      "specifications": null,
      "price": "129.99",
      "vendor": {userId},
      "category": {categoryId},
      "available": true,
      "quantity": 100,
      "rating": null,
      "total_reviews": 0
    }
    ```

    DELETE Request:

    ```bash
    curl -X DELETE localhost:8000/api/products/{productId} \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}"
    ```

    <aside>
    💡 In order to avoid breaking relationships with the product in the database, this request only sets the product as unavailable. The same result can be achieved using a PATCH request and setting the `available` field to `false`.

    </aside>

    DELETE Response (status code 200):

    ```json
    {
      "id": {productId},
      "name": "Headset Razer Kraken Ultimate",
      "brand": "Razer",
      "image_url": {imageURL},
      "description": "Headset description",
      "specifications": null,
      "price": "129.99",
      "vendor": {userId},
      "category": {categoryId},
      "available": false,
      "quantity": 100,
      "rating": null,
      "total_reviews": 0
    }
    ```


## Categories

- **Description**:  Allows the retrieval of the category list as well as the creation of new ones.
- **HTTP Methods**: GET, POST
- **URL**: localhost:8000/api/categories
- **Permissions**: Non-admin are not allowed to make POST requests.
- **Example**:

    GET Request:

    ```bash
    curl -X GET localhost:8000/api/categories \
       -H "Content-Type: application/json" \
    ```

    GET Response (status code 200):

    ```json
    [
      {
        "id": {categoryId},
        "name": "Gaming Accessories",
        "description": "Accessories about gaming, such as headsets, keyboards..."
      },
      {
        "id": {categoryId},
        "name": "classic Watches",
        "description": "Beautiful and stylish watches for modern women and men"
      }
    ]
    ```

    POST Request:

    ```bash
    curl -X POST localhost:8000/api/categories \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}" \
       -d '{"name": "Gaming Accessories", "description": "Accessories about gaming, such as headsets, keyboards..."}'
    ```

    POST Response (status code 201):

    ```json
    {
      "id": {categoryId},
      "name": "Gaming Accessories",
      "description": "Accessories about gaming, such as headsets, keyboards..."
    }
    ```


## Categories/{categoryId}

- **Description**:  Allows the retrieval, edition, and deletion of a category.
- **HTTP Methods**: GET, PATCH
- **URL**: localhost:8000/api/categories/{categoryId}
- ************************Permissions************************: Non-admins are not allowed to make PATCH and DELETE requests.
- **Example**:

    GET Request:

    ```bash
    curl -X GET localhost:8000/api/categories/{categoryId} \
       -H "Content-Type: application/json" \
    ```

    GET Response (status code 200):

    ```json
    {
      "id": {categoryId},
      "name": "Classic Women's Watches",
      "description": "Timeless watches for the modern woman"
    }
    ```

    PATCH Request:

    ```bash
    curl -X PATCH localhost:8000/api/categories/{categoryId} \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}" \
       -d '{"name": "Classic Women's Timepieces"}'
    ```

    PATCH Response (status code 200):

    ```json
    {
      "id": {categoryId},
      "name": "Classic Women's Timepieces",
      "description": "Timeless watches for the modern woman"
    }
    ```


## Inventory-items

- **Description**:  Allows the retrieval of the inventory items list. This endpoint is meant to be used by admins and vendors.
- **HTTP Methods**: GET
- **URL**: localhost:8000/api/inventory-items
- **Restriction**: Vendors can only retrieve the inventory items for their own products.
- **Example**:

    GET Request:

    ```bash
    curl -X GET localhost:8000/api/inventory-items \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}"
    ```

    GET Response (status code 200):

    ```json
    [
      {
        "id": {inventoryItemId},
        "product": {productId},
        "quantity": 10
      },
      {
        "id": {inventoryItemId},
        "product": {productId},
        "quantity": 5
      }
    ]
    ```


## Inventory-items/{inventoryItemId}

- **Description**:  Allows the retrieval of the inventory item list. This endpoint is meant to be used by admins and vendors.
- **HTTP Methods**: GET, PATCH
- **URL**: localhost:8000/api/inventory-items
- **Restriction**: Vendors can only retrieve the inventory items for their own products.
- **Example**:

    GET Request:

    ```bash
    curl -X GET localhost:8000/api/inventory-items/{inventoryItemId} \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}"
    ```

    GET Response (status code 200):

    ```json
    {
      "id": {inventoryItemId},
      "product": {productId},
      "quantity": 10
    }
    ```

    PATCH Request:

    ```bash
    curl -X PATCH localhost:8000/api/inventory-items/{inventoryItemId} \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}" \
       -d '{"quantity": 25}'
    ```

    PATCH Response (status code 200):

    ```json
    {
      "id": {inventoryItemId},
      "product": {productId},
      "quantity": 25
    }
    ```


## Cart

- **Description**:  Retrieves user’s shopping cart data.
- **HTTP Methods**: GET
- **URL**: localhost:8000/api/cart
- **Restriction**: Users can only see their own shopping carts.
- **Example**:

    GET Request:

    ```bash
    curl -X GET localhost:8000/api/cart \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}"
    ```

    GET Response (status code 200):

    ```json
    {
      "id": {cartId},
      "user": {userId},
      "cart_items": [
        {cartItemId},
        {cartItemId},
        {cartItemId}
      ],
      "total": 1497.0,
      "updated_on": "2023-05-17T18:27:15.028959Z"
    }
    ```


## Cart/items

- **Description**:  Allows the retrieval of the list of items as well as the addition of new ones in/to the user’s shopping cart.
- **HTTP Methods**: GET, POST
- **URL**: localhost:8000/api/cart/items
    - **Restriction**: Users can only access their own cart items.
- **Example**:

    GET Request:

    ```bash
    curl -X GET localhost:8000/api/cart/items \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}"
    ```

    GET Response (status code 200):

    ```json
    [
      {
        "id": {cartItemId},
        "cart": {cartId},
        "product": {productId},
        "quantity": 1,
        "sub_total": 499.0,
        "product_name": "Carbon (Gray Maple/Dark Gray)",
        "product_image": "/media/products/carbon_graymaple_darkgray.png",
        "product_brand": "Holzkern",
        "product_price": 499.0,
        "product_vendor": {userId},
        "product_available": true,
        "added_on": "2023-05-07T10:29:43.376720Z",
        "updated_on": "2023-05-07T10:29:43.376720Z"
      },
      {
        "id": {cartItemId},
        "cart": {cartId},
        "product": {productId},
        "quantity": 1,
        "sub_total": 499.0,
        "product_name": "Cobalt (Walnut/Blue)",
        "product_image": "/media/products/cobal_walnut_blue.jpg",
        "product_brand": "Holzkern",
        "product_price": 499.0,
        "product_vendor": {userId},
        "product_available": true,
        "added_on": "2023-05-12T10:37:29.555991Z",
        "updated_on": "2023-05-12T10:37:29.555991Z"
      },
      {
        "id": {cartItemId},
        "cart": {cartId},
        "product": {productId},
        "quantity": 1,
        "sub_total": 499.0,
        "product_name": "Argon (Leadwood/Silver)",
        "product_image": "/media/products/argon_leadwood_silver.png",
        "product_brand": "Holzkern",
        "product_price": 499.0,
        "product_vendor": {userId},
        "product_available": true,
        "added_on": "2023-05-17T18:27:15.028959Z",
        "updated_on": "2023-05-17T18:27:15.028959Z"
      }
    ]
    ```

    POST Request:

    ```bash
    curl -X POST localhost:8000/api/cart/items \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}" \
       -d '{"product": {productId}, "quantity": 1}'
    ```

    POST Response (status code 201):

    ```json
    {
      "id": {cartItemId},
      "cart": {cartId},
      "product": {productId},
      "quantity": 1,
      "sub_total": 1699.99,
      "product_name": "ASUS TUF Gaming A16 Advantage Edition (2023)",
      "product_image": "/media/products/A16_bg_kv_w8a7jPc.webp",
      "product_brand": "ASUS",
      "product_price": 1699.99,
      "product_vendor": {userId},
      "product_available": true,
      "added_on": "2023-05-22T15:07:59.863847Z",
      "updated_on": "2023-05-22T15:07:59.863858Z"
    }
    ```


## Cart/items/{cartItemId}

- **Description**:  Allows the retrieval, edition, and deletion of a cart item on the user’s shopping cart.
- **HTTP Methods**: GET, PATCH, DELETE
- **URL**: localhost:8000/api/cart/items/{cartItemId}
- **Restriction**: Users can only access their own cart items.
- **Example**:

    GET Request:

    ```bash
    curl -X GET localhost:8000/api/cart/items/{cartItemId} \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}"
    ```

    GET Response (status code 200):

    ```json
    {
      "id": {cartItemId},
      "cart": {cartId},
      "product": {productId},
      "quantity": 1,
      "sub_total": 1699.99,
      "product_name": "ASUS TUF Gaming A16 Advantage Edition (2023)",
      "product_image": "/media/products/A16_bg_kv_w8a7jPc.webp",
      "product_brand": "ASUS",
      "product_price": 1699.99,
      "product_vendor": {userId},
      "product_available": true,
      "added_on": "2023-05-22T15:15:18.355912Z",
      "updated_on": "2023-05-22T15:15:18.355919Z"
    }
    ```

    PATCH Request:

    ```bash
    curl -X PATCH localhost:8000/api/cart/items/{cartItemId} \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}" \
       -d '{"quantity": 2}'
    ```

    PATCH Response (status code 200):

    ```json
    {
      "id": {cartItemId},
      "cart": {cartId},
      "product": {productId},
      "quantity": 2,
      "sub_total": 3399.98,
      "product_name": "ASUS TUF Gaming A16 Advantage Edition (2023)",
      "product_image": "/media/products/A16_bg_kv_w8a7jPc.webp",
      "product_brand": "ASUS",
      "product_price": 1699.99,
      "product_vendor": {userId},
      "product_available": true,
      "added_on": "2023-05-22T15:07:59.863847Z",
      "updated_on": "2023-05-22T16:08:58.863858Z"
    }
    ```

    DELETE Request:

    ```bash
    curl -X DELETE localhost:8000/api/cart/items/{cartItemId} \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}"
    ```

    DELETE Response (status code 204):

    ```json
    []
    ```


## Orders

- **Description**:  Retrieves the user’s order list and creates new ones.
- **HTTP Methods**: GET, POST
- **URL**: localhost:8000/api/orders
- **Restriction**: Users can only access to their own orders.
- **Example**:

    GET Request:

    ```bash
    curl -X GET localhost:8000/api/orders \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {access_token}"
    ```

    GET Response (status code 200):

    ```json
    [
      {
        "id": {orderId},
        "user": {userId},
        "order_items": [
          {orderItemId},
          {orderItemId},
          {orderItemId}
        ],
        "total": 3038.98,
        "created_on": "2023-05-06T17:41:01.668524Z",
        "updated_on": "2023-05-06T17:41:01.668534Z"
      },
      {
        "id": {orderId},
        "user": {userId},
        "order_items": [
          {orderItemId},
          {orderItemId}
        ],
        "total": 2697.99,
        "created_on": "2023-05-07T21:04:03.068404Z",
        "updated_on": "2023-05-07T21:04:03.068426Z"
      }
    ]
    ```

    <aside>
    💡 Documentation for some of the endpoints is still missing. Such documentation will be added in the following days.

    </aside>