from marshmallow import post_load
from pillowtalk import *


def test_basic_schema():
    class Person(object):
        def __init__(self, id, name, address):
            vars(self).update(locals())

    class Address(object):
        def __init__(self, id, address_str):
            vars(self).update(locals())


    class PersonSchema(Schema):
        address = fields.Nested("AddressSchema")

        class Meta:
            additional = ["id", "name"]

        @post_load
        def make_person(self, data):
            return Person(**data)

    class AddressSchema(Schema):
        class Meta:
            additional = ["id", "address_str"]

        @post_load
        def make_address(self, data):
            return Address(**data)


    address_data = {
        "id"         : 3,
        "address_str": "NYC"
    }

    person_data = {
        "id"     : 5,
        "name"   : "Jeff",
        "address": address_data
    }

    p = PersonSchema().load(person_data).data
    schema = PersonSchema()
    x = 5