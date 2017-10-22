import pytest

from pillowtalk import *
from pillowtalk.schemas import add_schema


@pytest.fixture
def models(mybase):
    @add_schema
    class Person(mybase):
        items = []
        FIELDS = ["id", "name"]
        RELATIONSHIPS = [
            One("address", "find Person.address_id <> Address.id")
        ]

    @add_schema
    class Address(mybase):
        items = []
        FIELDS = ["id", "address_str"]
        ADDITIONAL_FIELDS = {
            "name": fields.String(required=False)
        }

    return Person, Address


def test_reference_retrieval(models):
    Person, Address = models

    person_data = {
        "name"      : "Richard",
        "id"        : 5,
        "address_id": 4
    }

    address_data = {
        "id"         : 4,
        "address_str": "Seattle, WA"
    }

    a = Address.load(address_data)
    p = Person.load(person_data)
    assert p.address == a


def test_reference_retrieval_none(models):
    Person, Address = models

    person_data = {
        "name"      : "Richard",
        "id"        : 5,
        "address_id": 6
    }

    address_data = {
        "id"         : 4,
        "address_str": "Seattle, WA"
    }

    a = Address.load(address_data)
    p = Person.load(person_data)
    a2 = p.address
    assert a2 is None

def test_load_address_with_json(models):
    Person, Address = models

    person_data = {
        "name"      : "Richard",
        "id"        : 5,
        "address": {
            "id": 4,
            "address_str": "Seattle, WA"
        }
    }

    p = Person.load(person_data)
    assert type(p.address) is Address