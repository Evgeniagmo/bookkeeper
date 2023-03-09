import sqlite3

from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T
from typing import Generic, TypeVar, Protocol, Any


class SQLiteRepository(AbstractRepository[T]):
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


        #with sqlite3.connect(self.db_file) as con:
        #    cur = con.cursor()
        #    cur.execute(f'DROP TABLE IF EXISTS {self.table_name}')
        #    cur.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} ({attributes})')
        #con.close()

    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({p})',
                values
            )
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        """ Получить объект по id """
        pass

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
            objs.append(self.cls(*tuple_obj))
        if where is None:
            return objs
        objs = [obj for obj in objs if
                all(getattr(obj, attr) == where[attr] for attr in where.keys())]
        return objs

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        pass

    def delete(self, pk: int) -> None:
        """ Удалить запись """

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'DELETE FROM {self.table_name} WHERE pk = {pk}')
        con.close()
