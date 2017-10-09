import inspect

from marshmallow import Schema, SchemaOpts, fields, post_load

from marshpillow.relationship import Relationship
import inflection

# TODO: Ability to add relationships without relationship string interpretation
# TODO: Wrap model collections in a class such that __getitem__ will fullfill the relationship...
# TODO: Inherit fields and relationships from super class
# TODO: Automatically load class when relationship is fullfilled so you don't have to code in cls.load(r) in the Base class you use
class MarshpillowError(Exception):
    """ Generic MarshpillowException """


class MarshpillowInitializerError(Exception):
    """ Generic initializer exception """


# TODO: Rename "RELATIONSHIPS", "FIELDS" to something shorter
# TODO: Raw isn't loading for many fields.Nested relationships
def validate_init(fxn):
    """ Raises errors for dynamically generated __init__ definitions """

    def wrapped(*args, **kwargs):
        self = args[0]
        args = args[1:]
        fields = self.__class__.FIELDS
        field_dict = {}
        if len(args) > len(fields):
            raise TypeError("Expected {0} arguments but got {1} for {2}.__init__".format(
                    len(fields), len(args), self.__class__.__name__))
        for i, a in enumerate(args):
            f = fields[i]
            field_dict[f] = a
        for k, v in kwargs.items():
            if k in field_dict:
                raise MarshpillowInitializerError("Got multiple values for {0}".format(k))
            else:
                field_dict[k] = v
        for f in fields:
            if f not in field_dict.keys():
                raise MarshpillowInitializerError("Missing argument for {0}".format(f))
        return fxn(self, (), **field_dict)

    return wrapped


class BaseSchemaOpts(SchemaOpts):
    """ Custom Schema options """

    def __init__(self, meta):
        super().__init__(meta)
        self.allow_none = getattr(meta, 'allow_none', ())


class BaseSchema(Schema):
    OPTIONS_CLASS = BaseSchemaOpts

    def on_bind_field(self, field_name, field_obj):
        """ dynamically allow_none for fields in the "allow_none" list in SchemaMeta """
        super().on_bind_field(field_name, field_obj)
        if field_name in self.opts.allow_none:
            field_obj.allow_none = True


def add_schema(cls, *args, **kwargs):
    """ Decorator that adds a dynamically generated schema to a model """

    # add model to Base.models
    MarshpillowBase.models[cls.__name__] = cls

    # automatically generated Schema
    class ModSchema(BaseSchema):

        relationships = {}

        class Meta:
            if hasattr(cls, "ALLOW_NONE"):
                allow_none = cls.ALLOW_NONE
            additional = cls.FIELDS
            ordered = True

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._clone_fields_from_model(cls)
            self._load_one_and_many()

        def _save_relationship(self, relation):
            self.__class__.relationships[relation.name] = relation
            if relation.attr1 not in self.fields:
                self.fields[relation.attr1] = fields.Raw()

        def _attach_model_to_relation(self, relation):
            if type(relation.mod2) is str:
                relation.mod2 = cls.get_model_by_name(relation.mod2)

        def _load_one_and_many(self):
            """ create nested fields from ONE and MANY """
            """
                Types of relationships:
                    ["Address"]
                    SmartRelation(mod1, attr1, etc.)
            """
            if hasattr(cls, "RELATIONSHIPS"):
                for relation in cls.RELATIONSHIPS:
                    model = None
                    attribute_name = None
                    many = False
                    if type(relation) is str:
                        attribute_name = relation
                        model = cls.get_model_by_name(attribute_name)
                    elif issubclass(relation.__class__, Relationship):
                        self._attach_model_to_relation(relation)
                        self._save_relationship(relation)
                        if relation.many:
                            many = True
                        model = relation.mod2
                        attribute_name = relation.name
                    self.fields[inflection.underscore(attribute_name)] = fields.Nested(model.Schema, many=many)

        def _clone_fields_from_model(self, model):
            """ Clone fields defined in model to model.Schema """
            for field_name, field in model.model_fields():
                self.fields[field_name] = field

        @post_load
        def make(self, data):
            try:
                model = cls(**data)
                return model
            except MarshpillowInitializerError as e:
                pass

    # end of ModeSchema

    cls.Schema = ModSchema
    return cls


class MarshpillowBase(object):
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
        if not hasattr(cls, "Schema") or cls.Schema is None:
            raise MarshpillowError("Schema not found. @add_schema may not have been added to class definition.")

    def __getattribute__(self, name):
        """ Called if attribute exists """
        schema_cls = object.__getattribute__(self, Schema.__name__)
        x = object.__getattribute__(self, name)
        if name in schema_cls.relationships:
            unmarshal = object.__getattribute__(self, MarshpillowBase.UNMARSHALL)
            if unmarshal:
                r = schema_cls.relationships[name]
                if type(x) is r.mod2:
                    return x
                else:
                    new_x = self.fullfill_relationship(name)
                    if new_x is not None and new_x != []:
                        x = new_x
        return x

    def __getattr__(self, name, saveattr=False):
        schema_cls = object.__getattribute__(self, Schema.__name__)
        if name in schema_cls.relationships:
            v = self.fullfill_relationship(name)
            if saveattr:
                setattr(self, name, v)
            return v
        v = object.__getattribute__(self, name)
        return v

    def _get_relationship(self, name):
        return self.Schema.relationships[name]

    def _has_relationship(self, name):
        schema_cls = object.__getattribute__(self, Schema.__name__)
        return name in schema_cls.relationships

    @classmethod
    def model_fields(cls):
        members = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        return [m for m in members if issubclass(m[1].__class__, fields.Field)]

    # TODO: Propogate attributes
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

    # def _parse_model_from_name(self, name):
    #     model_name = inflection.camelize(name)
    #     model = Base.models[model_name]
    #     model_id = getattr(self, name+"_id")
    #     m = model.find(model_id)
    #     setattr(self, name, m)
    #     return m

    @classmethod
    def to_model(cls, result, additional_opts=None):
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
        m = cls.to_model(data)
        m.raw = data
        cls._unlock_unmarshalling(m)
        return m

    @classmethod
    def json_to_models(cls, data):
        m = cls.to_model(data, {"many": True})
        for r, model in zip(data, m):
            model.raw = r
            cls._unlock_unmarshalling(model)
        return m

    def _lock_unmarshalling(self):
        object.__setattr__(self, MarshpillowBase.UNMARSHALL, False)

    def _unlock_unmarshalling(self):
        object.__setattr__(self, MarshpillowBase.UNMARSHALL, True)

    # def fullfill(self, name, relationship):
    #     if relationship.reference is None:
    #         # get from _id
    #         x = name+"_id"
    #         if hasattr(self, x):
    #             model_id = getattr(self, x)

    @classmethod
    def find(cls, id):
        raise NotImplementedError("method \"{0}\" is not yet implemented for {1}.".format("find", cls.__name__))

    @classmethod
    def where(cls, *args, **kwargs):
        raise NotImplementedError("method \"{0}\" is not yet implemented for {1}.".format("where", cls.__name__))

    @classmethod
    def all(cls):
        raise NotImplementedError("method \"{0}\" is not yet implemented for {1}.".format("all", cls.__name__))

    @classmethod
    def find_by_name(cls, name):
        raise NotImplementedError("method \"{0}\" is not yet implemented for {1}.".format("find_by_name", cls.__name__))

    def _propogate_attributes(self):
        """ Propogates attributes forward for vanilla Marshmallow objects and fullfilled relationship """

    def _add_promises(self):
        for name, relationship in self.__class__.Schema.relationships.items():
            setattr(self, name, self._get_relationship(name))


    # TODO: forward propogate properties if there is a relationship...from
    @classmethod
    def load(cls, data):
        """ Special load that will unmarshall dict objects or a list of dict objects """
        cls.check_for_schema()
        models = None
        if type(data) is list:
            models = cls.json_to_models(data)
            if len(models) > 0 and issubclass(models[0].__class__, MarshpillowBase):
                [m._add_promises() for m in models]

        elif type(data) is dict:
            models = cls.json_to_model(data)
        else:
            raise MarshpillowError("Data not recognized. Supply a dict or list: \"{0}\"".format(data))
        return models

    # TODO: Force unmarshalling of all or some of the relationships...
    def force(self):
        raise NotImplementedError("Force is not yet implemented")
