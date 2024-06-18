
# RESTful API for Library
This project is based on REST principles, implemented on Django framework and created to manage processes in the library.


## Features

- **Books** 
All users can familiarize themselves with the list of books. Only staff members can add new books.
- **Borrowings**
Registered users who have no payment debts can borrow books from the available books.
If a book is returned overdue, a fine is charged.
- **Payments**
After creating a Borrowing, the user is prompted to pay by Stripe, the payment session will be available within 24 hours
- **Authentication**
JWT authentication
- **Documentation**
Swagger, DRF Spectacular, Redoc
- **Scheduling**
Celery, Celery-beat
- **Notification**
The employee will receive the following notifications, with detailed information, in the Telegram chat:
1. When creating a Borrowing.
2. Upon successful payment.
3. A daily report of overdue borrowings and those about to become overdue.
4. Daily report of payments.
5. Monthly report of payments.


## Installation

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
### Example of environment variables
``` 
 .env.sample 
```

## Starting the server
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

Default superuser for testing

- **Email:** admin@admin.com
- **Password:** 1qazcde3

4. Start the development server:
```shell
python manage.py runserver
```

## Start tests
```shell
python manage.py test
```

## Run with Docker
```shell
docker-compose build  
```
```shell
docker-compose up 
```

### Getting access  
```
create user via api/user/register  
```
```
get access token via api/user/token  
```
```
    