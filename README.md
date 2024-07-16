# Проект: Веб-приложение для поиска и анализа вакансий

# Описание проекта
Веб-приложение на Django, которое позволяет пользователям искать вакансии по заданным параметрам и анализировать собранные данные. Пользователь вводит параметры для сайта с вакансиями, данные сохраняются в базу данных SQLite, и на другой странице выводится аналитика по вакансиям.

# Возможности
- Поиск вакансий по ключевым словам, городам, минимальной зарплате, образованию, опыту работы и периоду публикации.
- Сохранение данных о вакансиях в базу данных SQLite.
- Анализ данных с выводом средней, медианной, минимальной и максимальной зарплат.
- Запуск проекта с использованием Docker.

# Требования
- Docker
- Docker Compose

# Инструкции по запуску

Клонирование репозитория и запуск контейнеров
Для клонирования репозитория выполните следующие команды в терминале:


git clone https://github.com/Arturrybkin/sp24.git
cd parsing
Затем для построения и запуска контейнеров используйте команду:



docker-compose up --build
После этого вы сможете перейти на страницы приложения:
 • Страница поиска вакансий:http://127.0.0.1:8000/search/
 • Страница с анализом данных:http://127.0.0.1:8000/analytics/ (можно перейти по кнопке на странице поиска)
Структура проекта:
 • parsing/ - корневая директория проекта
 ◦ parser_app/ - приложение для парсинга вакансий и анализа данных
 ▪ migrations/ - миграции базы данных
 ▪ templates/ - HTML-шаблоны
 ▪ init.py
 ▪ admin.py
 ▪ apps.py
 ▪ forms.py - формы для ввода данных
 ▪ models.py - модели базы данных
 ▪ tests.py - тесты приложения
 ▪ views.py - представления для обработки логики приложения
 ◦ parsing/ - конфигурация проекта
 ▪ init.py
 ▪ asgi.py
 ▪ settings.py
 ▪ urls.py - маршрутизация URL
 ▪ wsgi.py
 ◦ db.sqlite3 - база данных SQLite
 ◦ manage.py - скрипт управления проектом Django
 ◦ requirements.txt - зависимости проекта
 ◦ Dockerfile - инструкции по созданию Docker-образа
 ◦ docker-compose.yml - конфигурация Docker Compose
