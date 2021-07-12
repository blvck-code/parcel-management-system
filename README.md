# Parcel Management System
[![Build Status](https://app.travis-ci.com/blvck-code/parcel-management-system.svg?branch=main)](https://app.travis-ci.com/blvck-code/parcel-management-system)
### This is a MVP project that deals with sending and closing dispatched parcels. It consists of the basic CRUD funtionality that allows teller/admin to dispatch parcels. 

### PMS is built with:
### 1. Angular (Frontend)
### 2. Flask (Backend)
## Want to check out this project?

Check out the [Parcel Management System](https://realpython.com/blog/python/token-based-authentication-with-flask/).

### Hosting Platforms
1. Frontend - Firebase
2. Backend - Heroku

## Want to use this project?

### 1. Frontend
### Basics

1. Fork/Clone
1. npm init

### Run the Application

```sh
$ ng serve
```

###Want to specify access as teller?

> [http://localhost:4200/](http://localhost:4200/)
> ```sh
> $ email: teller@gmail.com
> $ password: password
> ```

###Want to specify access as admin?

> [http://localhost:4200/backend/login](http://localhost:4200/backend/login)
> ```sh
> $ email: admin@gmail.com
> $ password: password
> ```
### 2. Backend
### Basics

1. Fork/Clone
1. Activate a virtualenv
1. Install the requirements

### Create DB

Create the databases in `sqlite`:

```sh
$ sqlite
# create database database.sqlite
```

Create the tables and run the migrations:

```sh
$ from project.server import db
$ db.create_all()
```

### Run the Application

```sh
$ python app.py
```

Access the application at the address [http://localhost:5000/](http://localhost:5000/)

> Want to specify a different port?

> ```sh
> $ python manage.py runserver -h 0.0.0.0 -p 8080
> ```

### Testing

Without coverage:

```sh
$ python manage.py test
$ OR
$ python manage.py cov
```

With coverage:

```sh
$ python manage.py cov
```
## Model Structure
![Models Diagram](https://user-images.githubusercontent.com/53207394/125304487-4fb60480-e336-11eb-8d44-7d91d500173b.jpg)

## Role Structure
![Roles](https://user-images.githubusercontent.com/53207394/125304589-652b2e80-e336-11eb-85ea-12d773aa5bd9.jpg)
