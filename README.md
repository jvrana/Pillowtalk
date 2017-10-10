# Marshpillow

Automatically creates intuitive python interfaces for APIs. Marshpillow talks to APIs and handles all of the model relationships behind the scenes, providing a clean and easy-to-use interface for your models.

# Why?

While there are plenty of excellent libraries for creating APIs, creating interfaces for these APIs isn't entirely straightforward. Marshpillow cleanly captures the underlying database relationships APIs may be providing making it easy to write python models. It provides a interface for making intuitive live API calls using your python models.

# Features

## Minimalistic models with relationships

e.g. Person with ONE Address; Address has MANY people
```python
class MyBase(MarshpillowBase):
    @classmethod
    def find(cls, id):
         ...
         
    def where(cls, data):
         ...

@add_schema
class Person(MyBase):
    FIELDS = ["id", "name"]
    RELATIONSHIPS = [
      One("address", "find Person.address_id <> Address.id")
    ]
      
@add_schema
class Address(MyBase):
    FIELDS = ["id", "str"]
    RELATIONSHIPS = [
      Many("people", "where Address.id <> Person.address_id")
    ]
```

Intuitive calls uses live API connection to deserialize data to your models

```python
# address.people doesn't exist yet
address = Address.find(3)

# calling .people causes a api call using "where" and deserialization of data
people = address.people # returns a list of People objects found through "where"

# returned is a list of Person objects!
assert type(people[0]) is Person 
```


Handling impartial data

```python
person = {
  "id": 5,
  "name": "Joe",
  "address": {"id": 4}
}

p = Person.load(person_data)

# a.address will magically return Address object even though data is enveloped in a json.
# we do not specifically have to handle deserialization of impartial data since the
# relationship between Person.address_id <> Address.id was already defined.
a = p.address
assert type(a) is Address
assert person.address_id == 4 # this wasn't defined explicitly but it is inferred from "address": {"id": 4}
```

## More examples and magic to come!
    Other things include:
        * Magic chaining in relationships
        * Session managing suggestions
        * automatically creating model skeletons from list of JSON
        * model relationships through associations
        * examples of connecting to MySQL or SQLlite
        * examples of using CLI through hug
        
