# RESTful API for Library 📚

## Overview 🔎

This project is a Django-based application that provides a REST API for managing a library's book borrowing system. The
API allows users to:

- View available books
- Borrow books
- Receive notifications on Telegram
- Make payments for borrowed books

The application ensures proper authentication and permissions to manage user access and actions.

## Table of Contents 📑

1. [Overview](#overview-)
2. [Features](#features-)
    - [Books](#books-)
    - [Borrowings](#borrowings-)
    - [Payments](#payments-)
    - [Authentication](#authentication-)
    - [Documentation](#documentation-)
    - [Scheduling](#scheduling-)
    - [Notifications](#notifications-)
3. [Installation](#installation-)
4. [Setting up Environment Variables](#setting-up-environment-variables)
5. [Starting the Server](#starting-the-server-)
6. [Run Tests](#run-tests-)
7. [Run with Docker](#run-with-docker-)
8. [Getting Access](#getting-access-)
9. [Contributing](#contributing-)

## Features

### Books 📚

- All users can browse the list of books.
- Only staff members can add new books to the library.

### Borrowings 🔄

- Registered users without outstanding payments can borrow available books.
- Overdue returns incur a fine.

### Payments 💳

- Users are prompted to pay via Stripe upon creating a borrowing.
- Payment sessions are valid for 24 hours.

### Authentication 🔐

- Secure JWT authentication for user access.

### Documentation 📑

- Comprehensive API documentation with Swagger, DRF Spectacular, and Redoc.

### Scheduling ⏰

- Task scheduling and automation using Celery and Celery Beat.

### Notifications 📬

- Detailed notifications for staff in the Telegram chat:
    1. Creation of a new borrowing.
    2. Successful payment.
    3. Daily report of overdue and soon-to-be overdue borrowings.
    4. Daily payment report.
    5. Monthly payment report.

## Installation 🔧

1. Clone the repository:

```shell
git clone https://github.com/DmytroHlazyrin/Library-service-api.git
```

2. Go to the project directory:

```shell
cd Library-service-api
```

3. Create and activate venv:

```shell
python -m venv venv 
source venv/bin/activate(on macOS)
venv\Scripts\activate(on Windows)
```

4. Set the project assignments:

```shell
pip install -r requirements.txt
```

### Setting up Environment Variables

```shell
touch .env  
```

#### Example of environment variables you can find in file:

``` 
 .env.sample 
```

## Starting the server 🚀

1. Create database migrations:

```shell
python manage.py makemigrations
python manage.py migrate
```

2. Create superuser:

```shell
python manage.py createsuperuser
```

3. *Load test data:

```shell
python manage.py loaddata library_service_db_data.json
```

Default superuser for testing 👤

- **Email:** admin@admin.com
- **Password:** 1qazcde3

4. Start the development server:

```shell
python manage.py runserver
```

## Run tests 🖋

```shell
python manage.py test
```

## Run with Docker 🐳

```shell
docker-compose build  
```

```shell
docker-compose up 
```

### Getting access 🔑

```
create user via api/user/register  
```

```
get access token via api/user/token  
```

## Contributing 🤝

We welcome contributions to improve this project! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push to your branch.
5. Create a pull request.

Please ensure your code adheres to our coding standards and includes appropriate tests.

## Conclusion 🎉

Thank you for checking out our Library Management System project! We hope this API makes it easier to manage book
borrowings, payments, and notifications in your library. With comprehensive features, secure authentication, and
detailed documentation, we strive to provide a robust and user-friendly solution.

Happy coding!
