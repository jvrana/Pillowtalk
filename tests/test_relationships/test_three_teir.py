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
            One("address", "find Person.address_id <> Address.id")
        ]

    @add_schema
    class Address(mybase):
        items = []
        FIELDS = ["id", "address_str"]
        RELATIONSHIPS = [
            One("street", "find Person.street_id <> Street.id")
        ]
    @add_schema
    class Street(mybase):
        items = []
        FIELDS = ["id", "name"]

    return Person, Address, Street

def test_main(models):
    Person, Address, Street = models


    street_data = {
        "id": 3,
        "name": "Colfax"
    }

    address_data = {
        "id": 3,
        "address_str": "Denver, CO",
        "street": street_data
    }

    person_data = {
        "id"     : 5,
        "name"   : "Jeff",
        "address": address_data
    }

    p = Person.load(person_data)
    assert type(p.address.street) is Street