# Mantella TMS

Mantella TMS (Test Management System) - API для управления тестированием. Это монолитный API с N-Tier архитектурой.

### Features
- Создание и контроль проектов для тестирования
- Определение Test Suites для группировки тест-кейсов и чел-листов
- Возможность прогонов (Test Runs) по тестовым артефактам 
- Ведение отчётности по найденным дефектам

### Stack
- fastapi+SQLAlchemy
- PostgreSQL
- NGINX

### Notes
Для запуска необходимо создать директорию ENV в src/backend, где будут храниться необходимые данные в виде переменных окружения.
1. `.env`
    - LEVEL=DEBUG - DEBUG|INFO
    - SECRET=mantella - секрет для генерации JWT
    - EMAIL_PASS= - пароль для отправки email уведомлений
2. `db.env`
    - DB_HOST=db - местоположение базы данных для подключения
    - DB_PORT=5432 - порт, который обслуживается БД
    - DB_USER=mantella - username пользователя БД
    - DB_PASS=mantella123321 - пароль пользователя БД
    - DB_NAME=mantella - название БД

Запустить приложение можно с помощью команды `docker-compose up`

- API - `http://localhost:8080/api`
- Docs - `http://localhost:8080/api/docs`
