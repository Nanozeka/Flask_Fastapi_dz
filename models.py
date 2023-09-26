# Задание №6
# Необходимо создать базу данных для интернет-магазина. База данных должна
# состоять из трех таблиц: товары, заказы и пользователи. Таблица товары должна
# содержать информацию о доступных товарах, их описаниях и ценах. Таблица
# пользователи должна содержать информацию о зарегистрированных
# пользователях магазина. Таблица заказы должна содержать информацию о
# заказах, сделанных пользователями.
# ○ Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY),
# имя, фамилия, адрес электронной почты и пароль.
# ○ Таблица товаров должна содержать следующие поля: id (PRIMARY KEY),
# название, описание и цена.
# ○ Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id
# пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус
# заказа.
#
# Создайте модели pydantic для получения новых данных и
# возврата существующих в БД для каждой из трёх таблиц
# (итого шесть моделей).
# Реализуйте CRUD операции для каждой из таблиц через
# создание маршрутов, REST API (итого 15 маршрутов).
# ○ Чтение всех
# ○ Чтение одного
# ○ Запись
# ○ Изменение
# ○ Удаление









from random import randint, choice
from typing import List
from datetime import date
from sqlalchemy import Date, func
import databases
import sqlalchemy
import fastapi
from sqlalchemy import ForeignKey
from pydantic import BaseModel
import uvicorn
from faker import Faker


DATABASE_URL = "sqlite:///my_database.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


app = fastapi.FastAPI()

# Создание полей в базе данных
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(32)),
    sqlalchemy.Column("last_name", sqlalchemy.String(52)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(132)),
    )


products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True),
    sqlalchemy.Column("product_name", sqlalchemy.String(320)),
    sqlalchemy.Column("description", sqlalchemy.String(1280000)),
    sqlalchemy.Column("price", sqlalchemy.Integer),
    )


orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, ForeignKey('users.id'), nullable=False),
    sqlalchemy.Column("product_id", sqlalchemy.Integer, ForeignKey('products.id'), nullable=False),
    sqlalchemy.Column("date_orders", Date, default=func.now()),
    sqlalchemy.Column("status_order", sqlalchemy.String(52)))

metadata.create_all(engine)


# Модели для таблицы users

class UserIn(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str


# Модели для таблицы products

class ProductIn(BaseModel):
    product_name: str
    description: str
    price: int


class Product(BaseModel):
    id: int
    product_name: str
    description: str
    price: int


# Модели для таблицы orders

class OrderIn(BaseModel):
    user_id: int
    product_id: int


class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    date_orders: date
    status_order: str


# @app.get("/fake_users/")
# async def fill_db():
#     faker = Faker()

  #   # Заполнение таблицы users
  #   for i in range(10):
  #       query = users.insert().values(
  #           first_name=faker.first_name(),
  #           last_name=faker.last_name(),
  #           email=faker.email(),
  #           password=faker.password()
  #       )
  #       await database.execute(query)
  #
  #
  #
  # # Заполнение таблицы products
  #   for i in range(10):
  #       query = products.insert().values(
  #           product_name=faker.word(),
  #           description=faker.text(),
  #           price=randint(100, 1000)
  #       )
  #       await database.execute(query)

# Заполнение таблицы orders
#     for i in range(50):
#         query = orders.insert().values(
#             user_id=randint(1, 10),
#             product_id=randint(1, 20),
#             date_orders=faker.date_between(start_date='-1y', end_date='today'),
#             status_order=choice(['new', 'processed', 'sent'])
#         )
#         await database.execute(query)



if __name__ == '__main__':
    uvicorn.run(
    "models:app",
    host="127.0.0.1",
    port=8040,
    reload=True
    )