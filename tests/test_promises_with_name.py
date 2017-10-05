from copy import copy
from marshmallow import pprint
import pytest

from marshpillow import *


@pytest.fixture
def models(mybase):

    @add_schema
    class Person(mybase):
        items = []
        FIELDS = ["id", "name"]
        RELATIONSHIPS = [
            SmartRelation("address", "find_by_name Person.address_name <> Address.name")
        ]

    @add_schema
    class Address(mybase):
        items = []
        name = fields.String(required=False)
        FIELDS = ["id", "address_str"]

    return Person, Address


def test_reference_retrieval(models):
    Person, Address = models

    person_data = {
        "name"      : "Richard",
        "id"        : 5,
        "address_name": "Richards house"
    }

    address_data = {
        "id"         : 4,
        "name": "Richards house",
        "address_str": "Seattle, WA"
    }

    a = Address.load(address_data)
    p = Person.load(person_data)
    assert p.address == a