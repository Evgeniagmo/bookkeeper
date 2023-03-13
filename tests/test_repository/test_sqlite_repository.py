from bookkeeper.repository.sqlite_repository import SQLiteRepository

import pytest

from dataclasses import dataclass

DB_NAME = r'D:\Py_project1\bookkeeper\test.db'


@pytest.fixture
def custom_class():
    @dataclass
    class Custom:
        text: str = 'abc'
        pk: int = 0

    return Custom


@pytest.fixture
def repo(custom_class):
    return SQLiteRepository(DB_NAME, custom_class)


def clear_all_data(repo):
    for obj in repo.get_all():
        repo.delete(obj.pk)


def test_crud(repo, custom_class):
    clear_all_data(repo)

    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk(repo, custom_class):
    clear_all_data(repo)

    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    clear_all_data(repo)

    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_delete_unexistent(repo):
    clear_all_data(repo)

    with pytest.raises(KeyError):
        repo.delete(1)


def test_cannot_update_without_pk(repo, custom_class):
    clear_all_data(repo)

    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_all(repo, custom_class):
    clear_all_data(repo)

    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects


def test_get_all_with_condition(repo, custom_class):
    clear_all_data(repo)

    objects = []
    for i in range(5):
        o = custom_class()
        o.text = 'test'
        repo.add(o)
        objects.append(o)
    assert repo.get_all({'pk': 5}) == [objects[4]]
    assert repo.get_all({'text': 'test'}) == objects
    assert repo.get_all({'pk': 1, 'text': 'test'}) == [objects[0]]
    assert repo.get_all({'text': 'no_test'}) == []
