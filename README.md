✈️ Travel Budget
Веб-сервис для планирования бюджета и трекинга расходов в путешествиях. Помогает контролировать финансы, конвертировать траты из разных валют в рубли и наглядно визуализировать статистику.
🌟 Основные возможности
Мультивалютность: Автоматическая конвертация трат в рубли по актуальному курсу.
Планирование: Установка бюджета поездки и отслеживание остатка.
Аналитика:
Интерактивные графики (Chart.js) для динамики расходов.
Статические диаграммы (Matplotlib) для отчетов.
Личный кабинет: Данные каждого пользователя изолированы.
Тёмная тема: Удобный интерфейс для любого времени суток.
🛠 Технологический стек
Backend: Python 3, Django 5
Database: PostgreSQL (Production) / SQLite (Dev)
Frontend: HTML5, Bootstrap 5, Chart.js
Аналитика: Matplotlib, Pandas (опционально)
API: ExchangeRate-API (курсы валют)

🚀 Как запустить проект
Клонируйте репозиторий:

git clone [https://github.com/h3nta123/travel-budget.git](https://github.com/h3nta123/travel-budget.git)
cd travel-budget


Установите зависимости:
pip install -r requirements.txt


Настройте переменные окружения:
Создайте файл .env в корне проекта (рядом с manage.py) и добавьте настройки базы данных:
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=your_secret_key
DB_NAME=travel_budget
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432


Примените миграции:
python manage.py migrate


Создайте суперпользователя:
python manage.py createsuperuser


Загрузите курсы валют:
python manage.py update_rates


Запустите сервер:
python manage.py runserver


Проект будет доступен по адресу: http://127.0.0.1:8000/
