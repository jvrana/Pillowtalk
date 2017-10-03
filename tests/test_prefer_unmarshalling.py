import pytest
from marshpillow import *

@pytest.fixture
def models(mybase):
    @add_schema
    class Person(mybase):
        items = []
        FIELDS = ["id", "name"]
        description = fields.String(required=False)
        # ADDITIONAL_FIELDS = dict(
        #         description=fields.String(required=False)
        # )
        RELATIONSHIPS = [
            HasOne("address", "address", "address", "find")
        ]
        # TODO: HasOne("address", "address", "address_id OR address["id"]", "find")
        # TODO: Multiple relationships?

    @add_schema
    class Address(mybase):
        items = []
        FIELDS = ["id", "address_str"]

    return Person, Address

def test_unmarshalling(models):
    Person, Address = models

    address_data = {
        "id"         : 3,
        "address_str": "Seattle, WA"
    }

    person_data = {
        "id"     : 5,
        "name"   : "Jeff",
        "address": address_data
    }

    p = Person.load(person_data)
    assert type(p.address) is Address

def test_unmarshall_from_incomplete_data(models):
    Person, Address = models

    address_data = {
        "id"         : 3
    }

    person_data = {
        "id"     : 5,
        "name"   : "Jeff",
        "address": address_data
    }

    p = Person.load(person_data)
    assert type(p.address) is Address
