class Person():
    FIELDS = ["id", "name"]
    MANY = [
        ("email", {"ref_model": "email", "ref": "person_id", "fxn": "where"}), # where Email.person_id == self.id
        ("budget", {"ref_model": "budget", "ref": "budget_id", "fxn": "where", "through": "budget_association"})
        # where Budget.id == BudgetAssociation.budget_id AND BudgetAssociation.person_id == self.id
    ]


class Email():
    FIELDS = ["id", "name"]
    ONE = [
        ("person", {"ref_model": "email", "ref": "person_id", "fxn": "find"}) # find Person.id == self.person_id
    ]


class BudgetAssociation():
    FIELDS = ["id"]
    ONE = [
        ("person", {"ref": "person_id", "fxn": "find"}), # find Person.id == self.person_id
        ("budget", {"ref": "budget_id", "fxn": "find"}) # find Budget.id == self.budget_id
    ]


class Budget():
    FIELDS = ["id", "name"]


budget = Budget.load(budget_data)
budget_associations = BudgetAssociation.load(budget_association_data)
emails = Email.load(email_data)
person = Person.load(person_data)

# has_many

# this_model: Person
# ref_model: Email
# ref: "person_id"
# fxn: "where"
# alias: where Email.person_id == person.id
person_emails1 = Email.where({"person_id": person.id})
person_emails2 = person.emails
assert set(person_emails1) == set(person_emails2)
# equivalent to: Email.where( {"person_id": p.id}

# this_model: Email
# ref_model: Person
# ref: "person_id"
# fxn: "find"
# alias: find Person.id == email.person_id
e = emails[0]
email_person1 = Person.find(e.person_id)
email_person2 = e.person
assert email_person1 == email_person2

# many-to-many
# this_model: Person
# ref_model: BudgetAssociation
# ref: "budget_id"
# fxn: "through association"
# params: BudgetAssociation, budget_id, person_id
# alias: where Budget.budget_id == BudgetAssociation.budget_id AND BudgetAssociation.person_id == Person.id
budget_associations = BudgetAssociation.where({"person_id": p.id})
budget_ids = [ba.budget_id for ba in budget_associations]
budgets1 = [Budget.find(x) for x in budget_ids]
budgets2 = p.budgets
assert budgets1 == budgets2
# equivalent to: Budget.find(BudgetAssociation.where( {"person_id": p.id} )
