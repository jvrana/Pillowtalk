import pytest
from marshpillow import *

def test(mybase):

    @add_schema
    class Person(mybase):
        items = []
        FIELDS = ["id", "name"]
        RELATIONSHIPS = [
            Association("budgets", "budget_association", "budget", "id", "where", "budget_id"), # many-to-many
            HasMany("emails", "email", "id", "where", "person_id")
        ]

    @add_schema
    class Budget(mybase):
        items = []
        FIELDS = ["id", "name"]
        RELATIONSHIPS = [
            Association("people", "budget_association", "person", "id", "where", "person_id") # many-to-many
        ]

    @add_schema
    class BudgetAssociation(mybase):
        items = []
        FIELDS = ["id"]
        RELATIONSHIPS = [
            HasOne("person", "person", "person_id", "find"),
            HasOne("budget", "budget", "budget_id", "find")
        ]

    @add_schema
    class Email(mybase):
        items = []
        FIELDS = ["id", "address"]
        RELATIONSHIPS = [
            HasOne("person", "person", "person_id", "find")
        ]

    people_data = [
        {"id": 5, "name": "Jill"},
        {"id": 6, "name": "John"},
        {"id": 7, "name": "JJ"}
    ]

    budgets_data = [
        {"id": 4, "name": "SD4"},
        {"id": 5, "name": "SD5"},
        {"id": 6, "name": "SD6"}
    ]

    association_data = [
        {"id": 1, "person_id": 5, "budget_id": 4},
        {"id": 2, "person_id": 5, "budget_id": 5},
        {"id": 3, "person_id": 6, "budget_id": 5},
        {"id": 4, "person_id": 7, "budget_id": 6}
    ]

    email_data = [
        {"id": 1, "address": "Jill@google.com", "person_id": 5},
        {"id": 2, "address": "John@google.com", "person_id": 6},
        {"id": 3, "address": "Jill+JUNK@hotmail.com", "person_id": 5}
    ]

    emails = Email.load(email_data)
    people = Person.load(people_data)
    associations = BudgetAssociation.load(association_data)
    budgets = Budget.load(budgets_data)

    jill = Person.find_by_name("Jill")
    assert jill.emails[0].person == jill

    assert len(jill.budgets) == 2






