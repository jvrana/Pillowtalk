import pytest
from pillowtalk import *


def test_too_many_relations():

    with pytest.raises(Exception):
        @add_schema
        class MyClasse(PillowtalkBase):
            FIELDS = []
            RELATIONSHIPS = [
                One("something", "find MyClasse.id <> Something.id <> SomethingElse.id <> Something")
            ]

def test_too_few_relations():

    with pytest.raises(Exception):
        @add_schema
        class MyClasse(PillowtalkBase):
            FIELDS = []
            RELATIONSHIPS = [
                One("something", "find MyClasse.id")
            ]

def test_missing_function():

    with pytest.raises(Exception):
        @add_schema
        class MyClasse(PillowtalkBase):
            FIELDS = []
            RELATIONSHIPS = [
                One("something", "MyClasse.id")
            ]