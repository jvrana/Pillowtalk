import pytest
from marshpillow import *

def test_basic(mybase):

    @add_schema
    class Email(mybase):
        items = []
        FIELDS = ["id", "address"]
        RELATIONSHIPS = [
            One("person", "find Email.person_id <> Person.id")
        ]

    @add_schema
    class Person(mybase):
        items = []
        FIELDS = ["id", "name"]
        RELATIONSHIPS = [
            Many("emails", "where Person.id <> Email.person_id")
        ]


    person_json = {"id": 5, "name": "Jill"}
    email_json = [
        {"id": 4, "address": "jill@hill.org", "person_id": 5},
        {"id": 5, "address": "jill2@hill.org", "person_id": 5},
        {"id": 6, "address": "jill3@hill.org", "person_id": 5}
    ]

    p = Person.load(person_json)
    emails = Email.load(email_json)
    p2 = emails[1].person
    assert p2 == p
    print(p.emails)
    person_emails = p.emails
    assert len(p.emails) == len(email_json)
