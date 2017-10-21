# `load(cls, data)`

1. Checks to make sure the Schema exists for the class (i.e. add_schema decorator is added)
1. If data is a list, then its interpreted as json_to_models
3. `json_to_model`
    1. calls `to_model`
    1. saves raw data.
    1. Marshalling is unlocked.
    1. returns the model
1. `to_model`
    1. loads the schema_opts()
    1. creates marshmallow schema using opts
    1. loads the schema using the data
    1. returns model

# getting attributes

If attribute exists, `__getattribute__(name)` is called.

```
schema_class = self.Schema
x = self.name
if name is in relationship names
    if marshalling is unlocked
        r = schema.relationships[name]
        get the relationship from the schema_class
        if x is is model expected from the relationship
            return x
        else
            x = fullfill_relationship(name)
            return x if not None
else
    return x
```

attempts to get name (__getattr__ runs if it cannot get it)
```
schema_class = self.Schema
if name is in relationship names
    v = fullfill_relationship(name)
    return v
v = object.__getattribute__(name)
return v
```

if name is the name found in a relationship:

If attribute does not exist, `__getattr__` is called