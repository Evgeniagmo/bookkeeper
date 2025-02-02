"""
Модуль для работы с базой данных с использованием СУБД sqlite3
"""

import sqlite3

from inspect import get_annotations
from typing import Any
from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """
    Класс репозитория, поддерживающий CRUD-операции на языке sqlite
    """

    db_file: str
    cls: type
    table_name: str
    fields: dict[str, Any]

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.cls = cls
        self.table_name = self.cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')

        attr_names = list(self.fields.keys())
        for name in range(len(attr_names)):
            attr_names[name] = str(attr_names[name])
        attr_values = list(self.fields.values())
        for val in range(len(attr_values)):
            if str(attr_values[val]).find('int') != -1:
                attr_values[val] = 'INTEGER'
            else:
                attr_values[val] = 'TEXT'
        attributes = list(n + ' ' + v for (n, v) in zip(attr_names, attr_values))
        attributes = ', '.join(['pk INTEGER PRIMARY KEY'] + attributes)
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            # cur.execute(f'DROP TABLE IF EXISTS {self.table_name}')
            cur.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} ({attributes})')
        con.close()

    def add(self, obj: T) -> int:
        """
        Добавить объект в репозиторий, вернуть id объекта,
        также записать id в атрибут pk.
        """

        if not hasattr(obj, 'pk'):
            raise ValueError("cannot add object without attribute pk")
        # if getattr(obj, 'pk') is not None:
        #    raise ValueError("cannot add object with defined attribute pk")
        if getattr(obj, 'pk', None) != 0:
            raise ValueError("cannot add object with defined attribute pk")
        names = ', '.join(self.fields.keys())
        place_holders = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({place_holders})',
                values
            )
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        """ Получить объект по id """

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'SELECT * FROM {self.table_name} WHERE pk = {pk}')
            tuple_obj = cur.fetchone()
        con.close()
        if tuple_obj is None:
            return None
        tuple_pk = int(tuple_obj[0])
        new_tuple_obj = list(tuple_obj)[1:]
        new_tuple_obj.append(tuple_pk)
        new_tuple_obj = tuple(new_tuple_obj)
        obj = self.cls(*new_tuple_obj)  # to avoid TestSQLiteRepo(pk=(1, ''), text='')
        return obj

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'SELECT * FROM {self.table_name}')
            tuple_objs = cur.fetchall()
        con.close()
        objs = []
        for tuple_obj in tuple_objs:
            tuple_pk = int(tuple_obj[0])
            new_tuple_obj = list(tuple_obj)[1:]
            new_tuple_obj.append(tuple_pk)
            new_tuple_obj = tuple(new_tuple_obj)
            objs.append(self.cls(*new_tuple_obj))
        if where is None:
            return objs
        objs = [obj for obj in objs if
                all(getattr(obj, attr) == where[attr] for attr in where.keys())]
        return objs

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """

        if obj.pk == 0:
            raise ValueError("object with unknown primary key")
        names = list(self.fields.keys())
        sets = ', '.join(f'{name} = \'{getattr(obj, name)}\'' for name in names)
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'UPDATE {self.table_name} SET {sets} WHERE pk = {obj.pk}')
        con.close()

    def delete(self, pk: int) -> None:
        """ Удалить запись """

        if self.get(pk) is None:
            raise KeyError("no object with such pk")
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'DELETE FROM {self.table_name} WHERE pk = {pk}')
        con.close()
