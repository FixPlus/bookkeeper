import sqlite3
import pytest
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from pprint import pprint


class SampleClass:
    def __init__(self, name: str, value1: int, value2: int):
        self.name = name
        self.value1 = value1
        self.value2 = value2

    def __eq__(self, other):
        return self.name == other.name and self.value1 == other.value1 and self.value2 == other.value2


@pytest.fixture(scope='function')
def sqlite_repo():
    repo = SQLiteRepository(':memory:', 'test_table', {'name': 'TEXT', 'value1': 'INTEGER', 'value2': 'INTEGER'}, SampleClass)
    yield repo
    repo.cursor.close()
    repo.connection.close()


def test_sqlite_repo_add(sqlite_repo):
    obj = SampleClass('test1', 1, 2)
    pk = sqlite_repo.add(obj)
    assert isinstance(pk, int) and pk > 0


def test_sqlite_repo_get(sqlite_repo):
    obj = SampleClass('test2', 3, 4)
    pk = sqlite_repo.add(obj)
    retrieved_obj = sqlite_repo.get(pk)
    assert retrieved_obj == obj


def test_sqlite_repo_get_all(sqlite_repo):
    obj1 = SampleClass('test3', 5, 6)
    obj2 = SampleClass('test4', 7, 8)
    sqlite_repo.add(obj1)
    sqlite_repo.add(obj2)
    objs = sqlite_repo.get_all()
    assert len(objs) == 2 and obj1 in objs and obj2 in objs


def test_sqlite_repo_get_all_with_where(sqlite_repo):
    obj1 = SampleClass('test5', 9, 10)
    obj2 = SampleClass('test6', 11, 12)
    sqlite_repo.add(obj1)
    sqlite_repo.add(obj2)
    where = {'name': 'test5'}
    objs = sqlite_repo.get_all(where)
    assert len(objs) == 1 and obj1 in objs and obj2 not in objs


def test_sqlite_repo_update(sqlite_repo):
    obj = SampleClass('test7', 13, 14)
    pk = sqlite_repo.add(obj)
    obj.value1 = 15
    sqlite_repo.update(obj)
    retrieved_obj = sqlite_repo.get(pk)
    assert retrieved_obj.value1 == 15


def test_sqlite_repo_delete(sqlite_repo):
    obj = SampleClass('test8', 16, 17)
    pk = sqlite_repo.add(obj)
    sqlite_repo.delete(pk)
    retrieved_obj = sqlite_repo.get(pk)
    assert retrieved_obj is None
