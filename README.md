# TeamProject
GoiTCursova

# PhotoShare

PhotoShare - це REST API для роботи зі світлинами, коментарями та профілями користувачів. Застосунок реалізований з використанням FastAPI.

## Функціонал

- **Аутентифікація**: JWT токени, ролі користувачів (звичайний, модератор, адміністратор).
- **Світлини**: Завантаження, редагування, видалення, теги, трансформації через Cloudinary, QR-коди.
- **Коментарі**: Додавання, редагування, видалення.
- **Профілі користувачів**: Редагування профілю, перегляд інформації.
- **Оцінки**: Виставлення рейтингів, перегляд середнього рейтингу.
- **Пошук і фільтрація**: Пошук світлин, фільтрація за рейтингом і датою.

## Налаштування

1. Скопіюйте `.env.example` в `.env` і налаштуйте змінні середовища.

2. Встановіть залежності:

   poetry init
   poetry shell
   poetry install
   
docker run --name postgres -e POSTGRES_DB=ProjectDB -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=567234 -p 5432:5432 -d postgres

poetry run alembic init alembic
poetry run alembic revision --autogenerate -m "Initial migration"
poetry run alembic upgrade head

poetry run uvicorn main:app --reload

=