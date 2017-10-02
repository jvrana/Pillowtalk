import pytest
from marshpillow import *

def test_basic(mybase):

    @add_schema
    class Budget(mybase):
        items = []
        FIELDS = ["id", "name"]
        RELATIONSHIPS = [
            Relationship("people", "budget_association", "id", "where", "budget_id", "person")
        ]

    @add_schema
    class BudgetAssociation(mybase):
        items = []
        FIELDS = ["id"]
        RELATIONSHIPS = [
            Relationship("person", "person", "person_id", "find"),
            Relationship("budget", "budget", "budget_id", "find")
        ]

    @add_schema
    class Person(mybase):
        items = []
        FIELDS = ["id", "name"]
        RELATIONSHIPS = [
            Relationship("budgets", "budget_association", "id", "where", "person_id", "budget")
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

    associations = [
        {"id": 1, "person_id": 5, "budget_id": 4},
        {"id": 2, "person_id": 5, "budget_id": 5},
        {"id": 3, "person_id": 6, "budget_id": 5},
        {"id": 4, "person_id": 7, "budget_id": 6}
    ]

    people = Person.load(people_data)
    budgets = Budget.load(budgets_data)
    budget_associations = BudgetAssociation.load(associations)

    # b = Budget.find(4)
    # assert len(b.people) == 1

    b = Budget.find(5)
    schema = Budget.Schema
    assert len(b.people) == 2

    b = Budget.find(6)
    assert len(b.people) == 1

    p = Person.find(5)
    assert len(p.budgets) == 2

    p = Person.find(6)
    assert len(p.budgets) == 1

    p = Person.find(7)
    assert len(p.budgets) == 1