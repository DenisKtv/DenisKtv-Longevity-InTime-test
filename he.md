# Task-Backend-1
# DenisKtv-longevity-intime-test - API

![example workflow](https://github.com/DenisKtv/DenisKtv-longevity-intime-test/actions/workflows/main.yml/badge.svg) 

## Technology Stack

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=django)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Celery](https://img.shields.io/badge/-Celery-464646?style=flat-square&logo=celery)](https://celeryproject.org/)
[![Redis](https://img.shields.io/badge/-Redis-464646?style=flat-square&logo=redis)](https://redis.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

## Project Description

The project implements a registration and authorization mechanism using an email address. Upon successful input of data that passes validation, the system using Celery and Redis sends a 6-digit code to the specified e-mail. After successful verification of the code, the user is given a token. With its help, as an authorized user, it is possible to view profiles, modify and delete your profile.

## Installing the project locally

* Склонировать репозиторий на локальную машину:
```bash
git clone https://github.com/DenisKtv/DenisKtv-test-referral.git
cd DenisKtv-test-referral/
```

* Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
. venv/bin/activate
```

* Cоздайте файл `.env` в директории `/infra/` с содержанием:

```
Django:
SECRET_KEY = 

telegram chat:
MY_CHAT = 
GROUP_ID =

Postgresql:
DB_ENGINE = 
DB_NAME = 
POSTGRES_USER = 
POSTGRES_PASSWORD = 
HOST = 
PORT = 
```

* Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

* Выполните миграции:

```bash
python manage.py migrate
```

* Запустите сервер:
```bash
python manage.py runserver
```

## Запуск проекта в Docker контейнере
* Установите Docker.

Параметры запуска описаны в файлах `docker-compose.yml` и `nginx.conf` которые находятся в директории `infra/`.  
При необходимости добавьте/измените адреса проекта в файле `nginx.conf`

* Запустите docker-compose:
```bash
docker-compose up -d --build
```  
  > После сборки появляются 3 контейнера:
  > 1. контейнер базы данных **db**
  > 2. контейнер приложения **web**
  > 3. контейнер web-сервера **nginx**
* Примените миграции:
```bash
docker-compose exec backend python manage.py migrate
```
* Создайте администратора:
```bash
docker-compose exec backend python manage.py createsuperuser
```
* Соберите статику:
```bash
docker-compose exec backend python manage.py collectstatic --no-input
```

## Страница для теста:
Страница доступна по ссылке:
[http://185.107.237.87:81/signup/](http://185.107.237.87:81/signup/)

## Документация к API:
API документация доступна по ссылке (создана с помощью redoc):
[http://185.107.237.87:81/redoc/](http://185.107.237.87:81/redoc/)

## Примеры запросов:

### http://185.107.237.87:81/signup/
<img src="images/1.png" alt="Alt text" title="Optional Title" width="250" /> <img src="images/2.png" alt="Alt text" title="Optional Title" width="250" /> <img src="images/1.1.png" alt="Alt text" title="Optional Title" width="300" />

### http://185.107.237.87:81/profile/
<img src="images/3.png" alt="Alt text" title="Optional Title" width="300" /> <img src="images/1.2.png" alt="Alt text" title="Optional Title" width="300" />
<img src="images/4.png" alt="Alt text" title="Optional Title" width="300" /> <img src="images/1.3.png" alt="Alt text" title="Optional Title" width="300" />

### http://185.107.237.87:81/referrals?phone_number=299345233
<img src="images/5.png" alt="Alt text" title="Optional Title" width="300" /> <img src="images/1.4.png" alt="Alt text" title="Optional Title" width="300" />