import pytest
from pillowtalk import *


@pytest.fixture(scope="module")
def mybase():
    class MyBase(PillowtalkBase):

        items = []

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__class__.items.append(self)

        @classmethod
        def find(cls, id):
            for i in cls.items:
                if i.id == id:
                    return i
            return None

        @classmethod
        def find_by_name(cls, name):
            for i in cls.items:
                if i.name == name:
                    return i
            return None

        @classmethod
        def where(cls, data):
            items = []
            for i in cls.items:
                passed = True
                for k, v in data.items():
                    if hasattr(i, k):
                        if not getattr(i, k) == v:
                            passed = False
                    else:
                        passed = False
                if passed:
                    items.append(i)
            return items
    return MyBase