import pytest
from marshpillow import *

def test_basic(mybase):

    @add_schema
    class Email(mybase):
        items = []
        FIELDS = ["id", "address"]
        RELATIONSHIPS = [
            Relationship("person", "person", "person_id", "find")
        ]

    @add_schema
    class Person(mybase):
        items = []
        FIELDS = ["id", "name"]
        RELATIONSHIPS = [
            Relationship("emails", "email", "id", "where", "person_id")
        ]


    person_json = {"id": 5, "name": "Jill"}
    email_json = [
        {"id": 4, "address": "jill@hill.org", "person_id": 5},
        {"id": 5, "address": "jill2@hill.org", "person_id": 5},
        {"id": 6, "address": "jill3@hill.org", "person_id": 5}
    ]

    p = Person.load(person_json)
    emails = Email.load(email_json)
    assert emails[1].person == p
    print(p.emails)
    person_emails = p.emails
    assert len(p.emails) == len(email_json)

    # TODO: C1 has many C2. By default, if C2 has one nested field referencing C1, than find all C2 with C1. Else
    # TODO: through error, UNLESS it is specified which attribute to use to reference
    # TODO: How to do associations???

