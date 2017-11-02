[![travis build](https://img.shields.io/travis/jvrana/Pillowtalk.svg)](https://travis-ci.org/jvrana/Pillowtalk)
[![Coverage Status](https://coveralls.io/repos/github/jvrana/Pillowtalk/badge.svg?branch=master)](https://coveralls.io/github/jvrana/Pillowtalk?branch=master)
[![PyPI version](https://badge.fury.io/py/pillowtalk.svg)](https://badge.fury.io/py/pillowtalk)

![pillow_talk_icon](images/pillowtalk_icon_medium.png?raw=true)

#### Build/Coverage Status
Branch | Build | Coverage
:---: | :---: | :---:
**master** | [![travis build](https://img.shields.io/travis/jvrana/Pillowtalk/master.svg)](https://travis-ci.org/jvrana/Pillowtalk/master) | [![Coverage Status](https://coveralls.io/repos/github/jvrana/Pillowtalk/badge.svg?branch=master)](https://coveralls.io/github/jvrana/Pillowtalk?branch=master)
**development** | [![travis build](https://img.shields.io/travis/jvrana/Pillowtalk/development.svg)](https://travis-ci.org/jvrana/Pillowtalk/development) | [![Coverage Status](https://coveralls.io/repos/github/jvrana/Pillowtalk/badge.svg?branch=development)](https://coveralls.io/github/jvrana/Pillowtalk?branch=development)

# **Pillowtalk**

Creates intuitive python wrappers for APIs. **Pillowtalk** talks to APIs and handles all of the model relationships behind the scenes, providing a clean and easy-to-use wrapper for your models.

# Why another package?

While there are plenty of excellent libraries for creating APIs, but creating intuitive wrappers for these APIs isn't entirely straightforward. **Pillowtalk** cleanly captures the underlying database relationships APIs may be providing making it easy to write python models. It provides a wrapper for making intuitive live API calls using your python models and the underlying relationships you specified.

In future versions, **pillowtalk** will be able to create and update your code based on a list of JSON files and *guess* at the underlying relationships between models. From there, **pillowtalk** will automatically generate or update python models. This means changes to some API can trigger an automatic update to your python wrapper to that API!

# Features and Examples

## Minimalistic models with relationships

e.g. Person with ONE Address; Address has MANY people
```python
class MyBase(PillowtalkBase):
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

## Session Management

Pillowtalk comes with a SessionManager class. Lets say you have an api connector:

```python
class MyAPI(object):

    def __init__(*args, **kwargs):
        self.__dict__.update(locals())
```

You can create a custom session manager easily by:

```python
class MySession(SessionManager):

    pass
```

You can register you connector by:
```python

# initialize your connectors
myapi = MyAPI(login="username", password="password", url="myurl")
myapi2 = MyAPI(login="username", password="password", url="myurl_2")

# register it
MySession().register_connector(myapi, session_name="session1")
MySession().register_connector(myapi, session_name="session2")
```

You can access your apis from anywhere by:

```python
# set to "session2"
MySession().set("session2")

# returns API associated with session1
MySession().session

# print the session_name
print(MySession().session_name)  # prints "session2"
```

SessionManager instances are a [Borg idioms](https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch05s23.html)
and share their state between instances:

```python
s1 = MySession()
s1.name = "something"
s2 = MySession()
s1.__dict__ == s2.__dict__
```

But not between other subclasses:
```python
s1 = MySession()
s1.name = "something"
s1.name != SessionManager().name
```

#### Saving and loading

SessionManager plays nicely with the pickle module. Save your sessions using `pickle.dump` and reload
your sessions with `pickle.load`. Loading will automatically update all of your session instances for your session class.

```python
import pickle

# save session info
with open(filepath, 'wb') as f:
    f.dump(MySession(), f)

# ...
# update session info
with open(filepath, 'rb') as f:
    f.load(f)
```

Optionally, `save` and `load` methods are included for convenience:

```python
MySession().save()

MySession().load()
```

## More examples and magic to come!
    Other things include:
        * Magic chaining in relationships
        * Session managing suggestions
        * automatically creating model skeletons from list of JSON
        * model relationships through associations
        * examples of connecting to MySQL or SQLlite
        * examples of using CLI through hug
        
