Установка

Клонируйте репозиторий:
git clone <URL-репозитория>
cd Django


Создайте виртуальное окружение:
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate


Установите зависимости:
pip install -r requirements.txt


Примените миграции базы данных:
python manage.py makemigrations
python manage.py migrate


Создайте суперпользователя для доступа к админке:
python manage.py createsuperuser

Следуйте инструкциям для создания имени пользователя, email и пароля.


Запуск проекта

Запустите сервер разработки:python manage.py runserver

Приложение будет доступно по адресу http://localhost:8000.

Доступ к админ-панели

Откройте браузер и перейдите по адресу:http://localhost:8000/admin/


Войдите, используя данные суперпользователя, созданные на этапе createsuperuser.
В админ-панели вы можете:
(В РАЗРАБОТКЕ)Управлять пользователями (например, создавать/редактировать гидов с их ролями, ID карты, Telegram-именем и полным именем).
Управлять экскурсиями (например, задавать дату, количество посетителей, назначать гида и привязывать к опросу).
Управлять опросами (например, создавать опросы для определённых недель и просматривать связанные экскурсии).
Фильтровать и искать данные (например, по имени гида, дате или статусу опроса).



Использование REST API
API доступен по адресу http://localhost:8000/api/.
Доступные эндпоинты

Экскурсии

GET /api/excursions/: Получить список всех экскурсий.
POST /api/excursions/: Создать новую экскурсию.{
  "date": "2025-10-27T11:00:00",
  "guide_id": "user1" (необязательный аргумент)
  "n_visitors": 15,
  "phone": "+1234567890",
  
}


GET /api/excursions//: Получить экскурсию по ID (например, /api/excursions/1/).{
        "id": 2,
        "date": "2025-10-27T14:59:00Z",
        "guide": "",
        "n_visitors": 20,
        "phone": "124",
        "poll": 1
}
Опросы

GET /api/polls/: Получить список всех опросов.
POST /api/polls/: Создать новый опрос (автоматически привязывает экскурсии за указанный период).{
  "week_start": "2025-10-20",
  "week_end": "2025-10-26"
}


GET /api/polls//: Получить опрос по ID (например, /api/polls/1/).{
        "id": 1,
        "week_start": "2025-10-24",
        "week_end": "2025-10-31",
        "is_active": true,
        "excursions": [
            {
                "id": 2,
                "date": "2025-10-27T14:59:00Z",
                "guide": "",
                "n_visitors": 20,
                "phone": "124",
                "poll": 1
            }
        ]
    }


Структура проекта
excursion_project/
├── manage.py
├── museumcrm/
│   ├── settings.py
│   ├── urls.py
├── api/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
└── requirements.txt

База данных

Используется SQLite (users.db) по умолчанию.
Модели: (В РАЗРАБОТКЕ)User, Excursion, Poll.
Связи:
Excursion связана с User (гид) и Poll через ForeignKey.
Poll имеет отношение "один-ко-многим" с Excursion (через related_name="excursions").
User имеет отношение "один-ко-многим" с Excursion (через related_name="excursions").



Примечания

Чтобы включить Browsable API (HTML-интерфейс для API), добавьте 'rest_framework.renderers.BrowsableAPIRenderer' в REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] в settings.py и настройте шаблоны.
