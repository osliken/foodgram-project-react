[![Main Kittygram workflow](https://github.com/osliken/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/osliken/foodgram-project-react/actions/workflows/main.yml)

# Foodgram - сервис "Продуктовый помощник"

## Описание проекта: 

Сервис Foodgram позволяет пользователям создавать свои кулинарные рецепты и публиковать их. Подписываться на публикации других пользователей и добавлять понравившиеся рецепты в "избранное". Но это ещё не всё, а чтобы не забыть какие же рецепты понравились, можно добавить их в список покупок и скачать его!

## Ссылка на приложение в сети:

[https://osliken.ru/](https://osliken.ru/)


## Стэк проекта:

- Git
- Docker
- Postgres
- Python 3.x
- Node.js 13.x.x
- Gunicorn
- Nginx
- Django
- React

## Локальный запуск проекта:

- Клонироуйте репозиторий:

    ```bash
    git clone git@github.com:osliken/foodgram-project-react.git
    ```
- Создайте файл .env

    ```bash
    touch .env
    ```
- Добавьте в файл .env переменные окружения:

    ```bash
    POSTGRES_USER=<имя пользователя>
    POSTGRES_PASSWORD=<пароль>
    POSTGRES_DB=<база данных>
    DB_NAME=<имя базы данных>
    DB_HOST=db
    DB_PORT=5432
    SECRET_KEY=<ключ Django>
    DEBUG=<True/False>
    ALLOWED_HOSTS=<localhost foodgram.ru>
    ```

## Документация к API доступна по адресу:

[https://osliken.ru/api/docs/](https://osliken.ru/api/docs/)


## Как развернуть проект на удалённом сервере:

- Скопируйте файл .env и docker-compose.production.yml в директорию проекта
- Запустите Docker compose

    ```bash
    sudo docker compose -f docker-compose.production.yml up -d
    ```
- Сделайте миграции и соберите статику

    ```bash
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
    sudo docker compose -f docker-compose.production.yml exec backend mkdir -p /backend_static/static/
    sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /static/static/
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py load_ingredients_data
    ```

## Автор

- Петров Сергей - [GitHub](https://github.com/osliken)
