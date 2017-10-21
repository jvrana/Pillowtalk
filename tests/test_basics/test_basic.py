import pytest
from marshmallow.exceptions import *

from marshpillow import *
from marshpillow.schemas import BaseSchema, add_schema


@pytest.fixture(scope="module")
def person_models(mybase):
    @add_schema
    class Person(mybase):
        items = []
        FIELDS = ["id", "name"]
        description = fields.String(required=False)
        # ADDITIONAL_FIELDS = dict(
        #         description=fields.String(required=False)
        # )
        RELATIONSHIPS = ["Address"]

    @add_schema
    class Address(mybase):
        items = []
        FIELDS = ["id", "address_str"]

    return Person, Address


@pytest.fixture(scope="function")
def person(person_models):
    Person, Address = person_models

    address_data = {
        "id"         : 3,
        "address_str": "NYC"
    }

    person_data = {
        "id"     : 5,
        "name"   : "Jeff",
        "address": address_data
    }

    p = Person.load(person_data)
    return p, person_data, address_data, Person, Address


def test_get_fields(person):
    p, person_data, address_data, Person, Address = person
    assert len(Person.model_fields()) == 1
    assert len(Address.model_fields()) == 0
    assert Person.model_fields()[0][0] == "description"


def test_basic_attributes(person):
    p, person_data, address_data, _, _ = person

    assert p.id == person_data["id"]
    assert p.name == person_data["name"]


def test_models_accessible_from_Base_class(person):
    p, person_data, address_data, Person, Address = person

    print(MarshpillowBase.models)
    for cls in [Person, Address]:
        name = cls.__name__
        assert name in MarshpillowBase.models
        assert MarshpillowBase.models[name] == cls


def test_schema_accessible_from_model(person):
    p, person_data, address_data, Person, Address = person

    assert issubclass(Person.Schema, BaseSchema)
    assert issubclass(Address.Schema, BaseSchema)
    assert Person.Schema is not Address.Schema


def test_accessible_nested_attribute(person):
    p, person_data, address_data, Person, Address = person
    s = Person.Schema()
    assert hasattr(p, "address")


def test_nested_attribute_unmarshalling(person):
    p, person_data, address_data, Person, Address = person
    print(p.address)
    assert type(p.address) is Address


def test_non_required_fields(person):
    p, person_data, address_data, Person, Address = person

    # re-load person
    person_data["description"] = "This is some description"
    p = Person.load(person_data)

    assert p.description == person_data["description"]


def test_non_strict(person):
    p, person_data, address_data, Person, Address = person

    # modify Person
    Person.description = fields.String(required=True)
    print(person_data)
    p = Person.load(person_data)


def test_strict(person):
    p, person_data, address_data, Person, Address = person

    Person.SCHEMA_OPTS = {"strict": True}

    # modify Person
    Person.description = fields.String(required=True)
    with pytest.raises(ValidationError):
        p = Person.load(person_data)


def test_with_using_find_function(mybase):
    @add_schema
    class Email(mybase):
        items = []
        FIELDS = ["id", "address"]

    @add_schema
    class Person(mybase):
        items = []
        FIELDS = ["id", "name"]
        RELATIONSHIPS = [
            One("email", "find Person.email_id <> Email.id")
        ]

    person_json = {"id": 5, "name": "Jill", "email_id": 4}
    email_json = {"id": 4, "address": "jill@hill.org"}

    e = Email.load(email_json)
    p = Person.load(person_json)

    assert p.email == e

def test_load_many(mybase):

    @add_schema
    class Email(mybase):
        items = []
        FIELDS = ["id", "address"]
        RELATIONSHIPS = [
            One("person", "find Email.person_id <> Person.id")
        ]

    email_json = [
        {"id": 4, "address": "jill@hill.org"},
        {"id": 5, "address": "jill2@hill.org"},
        {"id": 6, "address": "jill3@hill.org"}
    ]

    emails = Email.load(email_json)
    assert len(emails) == len(email_json)

def test_additional_fields(mybase):

    @add_schema
    class Email(mybase):
        items = []
        FIELDS = ["id", "address"]
        RELATIONSHIPS = [
            One("person", "find Email.person_id <> Person.id")
        ]

    email_json = {"id": 4, "address": "jill@hill.org", "additional_field": 6}

    email = Email.load(email_json)
    print(email.additional_field)


    # assert p.description == person_data["description"]