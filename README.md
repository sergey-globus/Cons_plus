# Правовой портал - Django веб-приложение

Современный веб-портал для предоставления юридических услуг с функциями консультаций, генерации документов, FAQ и аналитики.

## Возможности

- 📋 **FAQ система** - часто задаваемые вопросы с категориями
- 💬 **Консультации** - форма для связи с юристами
- 📄 **Генератор документов** - создание документов по шаблонам
- 👥 **Система пользователей** - регистрация, авторизация, профили
- 📊 **Аналитика** - отслеживание посещений и статистика
- 🗞️ **Правовые новости** - интеграция с внешними API
- 🔧 **Админ-панель** - управление контентом

## Технологии

- **Backend**: Django 4.2.7, Python 3.8+
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **API**: REST API для внешних интеграций

## Установка и запуск

### Предварительные требования

- Python 3.8 или выше
- Git (опционально)

1.  **Клонируйте репозиторий:**

    ```
    git clone https://git.nlmk.com/wms-coilyard-hrm/l2/nlmk-mes-umsklad-optimizationservice.git
    cd .\nlmk-mes-umsklad-optimizationservice\
    git checkout dev
    ```
2. **Создайте и активируйте виртуальное окружение:**

    *   Создайте виртуальное окружение с помощью команды:

        ```
        python -m venv .venv
        ```

    *   Активируйте виртуальное окружение 
        
        ```
        source venv/Scripts/activate
        ``` 

3.  **Установите зависимости:**

    ```
    pip install -r requirements.txt
    ```

4.  **Создайте миграции:**

    ```
    python manage.py makemigrations main
    python manage.py makemigrations users  
    python manage.py makemigrations analytics
    ```

5.  **Примените миграции:**

    ```
    python manage.py migrate
    ```

6.  **Создайте суперпользователя**

    ```
    python manage.py createsuperuser
    ```
    Username: введите например 1
    Email address: 1@mail.com
    Password: 1

7.  **Запустите приложение:**

    ```
    python manage.py runserver
    ```

7.  **Откройте хост:**

    - После запуска приложения откройте в браузере адрес: `http://127.0.0.1:8000/`.

    