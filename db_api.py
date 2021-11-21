# - *- coding: utf- 8 - *-
import random
import sqlite3
import time
from sqlite3 import IntegrityError
import config

# Путь к БД

####################################################################################################
###################################### ФОРМАТИРОВАНИЕ ЗАПРОСА ######################################
# Форматирование запроса с аргументами
def update_format_with_args(sql, parameters: dict):
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)
    return sql, tuple(parameters.values())


# Форматирование запроса без аргументов
def get_format_args(sql, parameters: dict):
    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])
    return sql, tuple(parameters.values())


####################################################################################################
########################################### ЗАПРОСЫ К БД ###########################################
# Добавление данных в таблицы
def add_user(id, username, full_name, registration_date, language):
    try:
        with sqlite3.connect(config.path_to_db) as db:
            db.execute("INSERT INTO users "
                       "(id, username, full_name, registration_date, language) "
                       "VALUES (?, ?, ?, ?, ?)",
                       [id, username, full_name, registration_date, language])
            db.commit()
    except sqlite3.IntegrityError:
        pass


def add_files_data(file_name, file_url, upload_date, owner):
    try:
        with sqlite3.connect(config.path_to_db) as db:
            db.execute("INSERT INTO files_data "
                       "(file_name, file_url, upload_date, owner) "
                       "VALUES (?, ?, ?, ?)",
                       [file_name, file_url, upload_date, owner])
            db.commit()
    except sqlite3.IntegrityError:
        pass


def get_all_files_data():
    with sqlite3.connect(config.path_to_db) as db:
        sql = "SELECT * FROM files_data "
        return db.execute(sql).fetchall()


def get_user_files_data(**kwargs):
    with sqlite3.connect(config.path_to_db) as db:
        sql = "SELECT * FROM files_data WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        return db.execute(sql, parameters).fetchall()


def delete_files_data(**kwargs):
    with sqlite3.connect(config.path_to_db) as db:
        sql = "DELETE FROM files_data WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()


# Получение пользователей
def get_all_users():
    with sqlite3.connect(config.path_to_db) as db:
        sql = "SELECT * FROM users "
        return db.execute(sql).fetchall()


def get_user(**kwargs):
    with sqlite3.connect(config.path_to_db) as db:
        sql = "SELECT * FROM users WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        return db.execute(sql, parameters).fetchone()


def get_users(**kwargs):
    with sqlite3.connect(config.path_to_db) as db:
        sql = "SELECT * FROM users WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        return db.execute(sql, parameters).fetchall()

def update_user(id, **kwargs):
    with sqlite3.connect(config.path_to_db) as db:
        sql = f"UPDATE users SET XXX WHERE id = {id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()
