## Задачи
Опишите Dockerfile для запуска контейнера с проектом.

Оберните в Docker Compose Django-проект с БД PostgreSQL.

Допишите в docker-compose.yaml работу с Redis.

Допишите в docker-compose.yaml работу с Celery.

### Необходимо создать файл 
.env и заполнить своими данными (на примере файла .env.sample)

### Создание и запуск контейнеров
docker-compose up -d --build

### Создание суперпользователя
docker exec -it drf_homework-app-1 python manage.py csu

