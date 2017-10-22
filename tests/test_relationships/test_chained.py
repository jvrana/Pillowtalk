from pillowtalk import *
from pillowtalk.schemas import add_schema


def test(mybase):

    @add_schema
    class Person(mybase):
        items = []
        FIELDS = ["id", "name"]
        RELATIONSHIPS = [
            Many("emails", "where Person.id <> Email.person.id")
        ]

    @add_schema
    class Email(mybase):
        items = []
        FIELDS = ["id", "name"]
        RELATIONSHIPS = [
            One("person", "find Email.person <> Person.id")
        ]

    person_data = {
        "id": 1,
        "name": "John"
    }

    email_data = {
        "id": 2,
        "name": "john@uw.edu",
        "person": {
            "id": 1
        }
    }

    e = Email.load(email_data)
    print(e.person)
    p = Person.load(person_data)

    assert e.person == p

