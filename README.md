# **Marshpillow**

**Marshpillow** is a small framework for interacting with APIs. **Marshpillow** generates ORM python models and schemas for interacting with APIs. It can even *guess* the object relations from a JSON file and automatically generate a code skeletons for those relations

## Why another library? (better description pending...)
Theres lots of libraries for creating APIs but not alot of libraries for interacting with those APIs. Behind most APIs is an underlying object relation structure (hopefully!). **Marshpillow** guesses these relations and tries to deserialize data on-the-fly through an API connection to as app, website, or database. 

The goals of **Marshpillow** is to create python models that:
* are compact
* are easily scalable
* are easily maintained through changes to some API
* have a live connection to an API

## Status

V0.0.1 - New and in progress (aka probably don't use it yet)

## What it does

JSON files can be generated from any API, **Marshpillow** will generate a code skeleton
for marshalling/unmarshalling to generated python models.

* Have an API you want to work with?
* Want to quickly create custom models that can be serialized and descerialized?
* Are you too lazy and/or busy to write your own code?
* Want to procedurally generate code for models from a JSON file?
* Want your models to easily update based on changes to API?

Script to connect to API and automatically update models...

While there are lots of packages and frameworks for generating APIs, there are not very many
for interacting with already created APIs. **Marshpillow** bridges this gap between API-python-API.

**Marshpillow** is a light framework for automatically creating marshmallow schemas. It is
database, ORM agnostic.

### Quickly create models/schemas...
```python
@add_schema
class Person(object)
    FIELDS = ["id", "name", "description"]
    ONE = [("address", {through: "address_association"}]
    MANY = [("person", {as: "friend"})]

    def text_friends(self, msg):
        pass

@add_schema
class Address(object)
    FIELDS = ["id", "address_str"]

@add_schema
class AddressAssociation:
""" Details a Person:Address association """
       FIELDS = []
       ONE = ["person", "address"]

address = {
    "id": 1,
    "address_str": "101 Central Park, NYC, USA"
}

address_association = {
    "person": 1,
    "address": 1,
    "id": 3
}

person_data = {
    "id": 1,
    "name": "Jerry",
    "friends": [1,2,3,4]
    "address_association": 3
}
```

### Magically marshal associated models on the fly through database connection!

```python
p = Person.load(person_data)
p.friends # returns list of Person models accessed through the database through the id references
p.address # returns Address model through the AddressAssociation model gather from the database
```

Notice how there was no real reference to the address data in the person data. Marshpillow magically used a API connection
to find the address_data and unmarshall it to an Address object!

### TODO: Show that Marshpillow works like a regular Marshmallow Schema/Model### 
### TODO: New name? Marsupial? Marshsupial? MarshSoupial? (I like Marsupial...could have a picture of a koala...)\

Create new instances and dump them to JSON
```python
a = Address(address_str="Somewhere in Seattle, WA")
p = Person(name: "Justin", address=a)

Person.dump(p) # dumps Person model to JSON

{
    name: "Justin",
    address: {
        address_str: "Somewhere in Seattle, WA"
    }
}

{
    "Person": {

    }
    "Address": {

    }
    "AddressAssociation": {
        person: Person
        address: Address
    }
}

```
