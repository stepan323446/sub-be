# SubTrack (Backend Part)

This is the backend part of web application **SubTrack** which is based on Django Rest Framework (Python)

Frontend part: [sub-fe (Github)](https://github.com/stepan323446/sub-fe)

## Project Overview

SubTrack Backend provides APIs for managing and tracking subscription services (Spotify, YouTube), with integration of the Exchange Rate API to get up-to-date currency prices.

## Features

* User authentication with JWT and Google OAuth
* Swagger as a documentation for API endpoints
* Integration with Exchange Rate API
* GithHub CI/CD
* Docker installation
* Django Rest Framework and django-filters
* Cron Job

## Settings and Entry Points

Project has two entry points: `manage.py` and `manage_dev.py`. In the project folder (`project/settings/`), there are also three files:

* `base.py` - Main configuration. All key settings for the Django project are defined here.
* `dev.py` - Imports all main settings from base.py and overrides some variables for development on localhost.
* `prod.py` - Also imports all main settings from base.py and overrides variables for production.

Depending on the chosen entry point, the corresponding configuration will be used.

*P.s. To interact with variables from different Django apps, use `project/settings_context.py`*

## Installing

1. Clone repository
```shell
git clone https://github.com/stepan323446/sub-be.git
```
2. Create new virtualenv and install requirements
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements
```
3. (production) If you use MySQL, you need to install `mysqlclient`
```shell
pip install mysqlclient
```
4. Create a `.env` file and add the following variables. EXCHANGE_RATE_KEY is the API key provided by [Exchange Rate API](https://www.exchangerate-api.com/)
```
SECRET_KEY=
EMAIL_HOST_USER=test@email.com
EMAIL_HOST_PASSWORD=
EXCHANGE_RATE_KEY=
FRONTEND_DOMAIN=localhost:3000
PROD_DB_NAME=
PROD_DB_USER=
PROD_DB_PASS=
```
5. Run the migrations. Depending on your needs, choose the appropriate entry point. Here, I will use `manage_dev.py`
```shell
python3 manage_dev.py migrate
```
6. Run server
```shell
python3 manage_dev.py runserver
```

*P.s. To see all API endpoints, go to `localhost:8000/swagger`*