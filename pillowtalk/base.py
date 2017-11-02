import inspect

import inflection
from marshmallow import Schema, fields

from pillowtalk.exceptions import PillowtalkError
from pillowtalk.relationship import Relationship
from pillowtalk.utils import validate_init


# TODO: Ability to add relationships without relationship string interpretation
# TODO: Wrap model collections in a class such that __getitem__ will fullfill the relationship...
# TODO: Inherit fields and relationships from super class
# TODO: Automatically load class when relationship is fullfilled so you don't have to code in cls.load(r) in the Base class you use
# TODO: partially unmarshalled lists, when calling [i] is will update the object on the fly...
# TODO: needs to know when object is deserialized completely.

class APIInterface(object):
    @classmethod
    def find(cls, *args, **kwargs):
        raise NotImplementedError("method \"{0}\" is not yet implemented for {1}.".format("find", cls.__name__))

    @classmethod
    def where(cls, *args, **kwargs):
        raise NotImplementedError("method \"{0}\" is not yet implemented for {1}.".format("where", cls.__name__))

    @classmethod
    def all(cls):
        raise NotImplementedError("method \"{0}\" is not yet implemented for {1}.".format("all", cls.__name__))

    @classmethod
    def find_by_name(cls, *args, **kwargs):
        raise NotImplementedError("method \"{0}\" is not yet implemented for {1}.".format("find_by_name", cls.__name__))

    def update(cls, *args, **kwargs):
        # self.__dict__.update(self.__class__.find(self.id).__dict__)
        raise NotImplementedError("method \"{0}\" is not yet implemented for {1}.".format("update", cls.__name__))

    # TODO: Force unmarshalling of all or some of the relationships...
    def force(self):
        raise NotImplementedError("Force is not yet implemented")


class PillowtalkBase(APIInterface, object):
    """ Basic model for api items """

    Schema = None
    models = {}
    UNMARSHALL = "_unmarshall"

    @validate_init
    def __init__(self, *args, **kwargs):
        vars(self).update(kwargs)
        self.raw = None
        self.__class__.check_for_schema()
        self._unmarshall = False

    @classmethod
    def check_for_schema(cls):
        """ Checks to see if class has a Schema """
        if not hasattr(cls, "Schema") or cls.Schema is None:
            raise PillowtalkError("Schema not found. @add_schema may not have been added to class definition.")

    def __getattribute__(self, name):
        """ Override for attributes. If attribute is found and attribute is a relationship, an attempt to fullfill
         the relationship will be made. """
        x = object.__getattribute__(self, name)
        if name.startswith("_"):
            return x
        schema_cls = object.__getattribute__(self, Schema.__name__)
        if name in schema_cls.relationships:
            if object.__getattribute__(self, PillowtalkBase.UNMARSHALL):  # locking marshalling prevents recursion
                # Decide to use original value or fullfilled value...
                r = schema_cls.relationships[name]
                if type(x) is r.mod2:  # if relationship is already fullfilled
                    return x
                else:
                    new_x = self.fullfill_relationship(name)
                    if new_x is not None and new_x != [None] and new_x != []:
                        return new_x
        if issubclass(x.__class__, Relationship):
            raise TypeError("Relationship \"name\" was not correctly resolved.")
        return x

    def __getattr__(self, name, saveattr=False):
        """ If attribute is not found, attempts to fullfill the relationship """
        schema_cls = object.__getattribute__(self, Schema.__name__)
        if name in schema_cls.relationships:
            v = self.fullfill_relationship(name)
            if saveattr:
                setattr(self, name, v)
            return v
        # TODO: if attribute doesn't exist, attempt to update from database
        v = object.__getattribute__(self, name)
        return v

    def _get_relationship(self, name):
        return self.Schema.relationships[name]

    # def _has_relationship(self, name):
    #     schema_cls = object.__getattribute__(self, Schema.__name__)
    #     return name in schema_cls.relationships

    @classmethod
    def model_fields(cls):
        """ Returns the models fields """
        members = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        return [m for m in members if issubclass(m[1].__class__, fields.Field)]

    def fullfill_relationship(self, relationship_name):
        """
        Fullfills a relationship using "using", "ref", "fxn."

        Sample
            Promise("sample_type", <SampleType>, "sample_type_id", "find")
        """
        relationship = self._get_relationship(relationship_name)
        self._lock_unmarshalling()
        x = relationship.fullfill(self)
        self._unlock_unmarshalling()
        return x

    @classmethod
    def to_model(cls, result, additional_opts=None):
        """ Loads model from result using Marshmallow schema located in cls.Schema """
        opts = {}
        opts.update(cls.get_schema_opts())
        if additional_opts is not None:
            opts.update(additional_opts)
        schema = cls.Schema(**opts)
        model, errors = schema.load(result)
        return model

    @classmethod
    def get_model_by_name(cls, name):
        """ Converts a snake_case model name to the model object """
        model_name = inflection.camelize(name)  # class name of the model to use
        model = cls.models[model_name]
        return model

    @classmethod
    def get_schema_opts(cls):
        if hasattr(cls, "SCHEMA_OPTS"):
            return cls.SCHEMA_OPTS
        else:
            return {}

    @classmethod
    def json_to_model(cls, data):
        """ Converts a json to a model using a Schema """
        m = cls.to_model(data)
        m.raw = data
        cls._unlock_unmarshalling(m)
        cls.set_additional_fields(m, data)
        return m

    @classmethod
    def json_to_models(cls, data):
        """ Converts a list of json to a list of models using a Schema """
        models = cls.to_model(data, {"many": True})
        for model_data, model in zip(data, models):
            model.raw = model_data
            cls._unlock_unmarshalling(model)
            cls.set_additional_fields(model, model_data)
        return models

    def _lock_unmarshalling(self):
        """ locks model so relationships cannot be fullfilled. Prevents recursion. """
        object.__setattr__(self, PillowtalkBase.UNMARSHALL, False)

    def _unlock_unmarshalling(self):
        """ unlocks model so relationships can be fullfilled. """
        object.__setattr__(self, PillowtalkBase.UNMARSHALL, True)

    # def _add_relationships(self):
    #     """ Copies relationship found in the Schema to this instance """
    #     for name, relationship in self.__class__.Schema.relationships.items():
    #         setattr(self, name, self._get_relationship(name))

    @classmethod
    def set_additional_fields(cls, model, data):
        """ Set attributes for additional fields not found in the Schema or model definition """
        for k, v in data.items():
            if not hasattr(model, k):
                setattr(model, k, v)

    # TODO: forward propogate properties if there is a relationship...from
    @classmethod
    def load(cls, data):
        """ Special load that will unmarshall dict objects or a list of dict objects """
        cls.check_for_schema()
        models = None
        if type(data) is list:
            models = cls.json_to_models(data)
            # if len(models) > 0 and issubclass(models[0].__class__, PillowtalkBase):
            #     # [m._add_relationships() for m in models]
        elif type(data) is dict:
            models = cls.json_to_model(data)
        else:
            raise PillowtalkError("Data not recognized. Supply a dict or list: \"{0}\"".format(data))
        return models

    def dump(self):
        s = self.__class__.Schema()
        return s.dump(self).data
