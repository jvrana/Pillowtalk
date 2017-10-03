import inspect

from marshmallow import Schema, SchemaOpts, fields, post_load

from marshpillow.relationship import Association, HasMany, Relationship
from marshpillow.utils import utils


class MarshpillowError(Exception):
    """ Generic MarshpillowException """

class MarshpillowInitializerError(Exception):
    """ Generic initializer exception """

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
    Base.models[cls.__name__] = cls

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
            self.__class__.relationships[relation.attribute] = relation
            if relation.with_reference not in self.fields:
                self.fields[relation.with_reference] = fields.Raw()

        def _attach_model_to_relation(self, relation):
            if type(relation.with_model) is str:
                relation.with_model = cls.get_model_by_name(relation.with_model)

        def _load_one_and_many(self):
            """ create nested fields from ONE and MANY """
            if hasattr(cls, "RELATIONSHIPS"):
                for relation in cls.RELATIONSHIPS:
                    many = False
                    model_name = relation
                    if issubclass(relation.__class__, Relationship):
                        model_name = relation.with_model
                        self._attach_model_to_relation(relation)
                        self._save_relationship(relation)
                        if type(relation) is HasMany or type(relation) is Association:
                            many = True
                    schema = cls.get_model_by_name(model_name).Schema
                    self.fields[model_name] = fields.Nested(schema, many=many)

        def _clone_fields_from_model(self, model):
            """ Clone fields defined in model to model.Schema """
            for field_name, field in model.model_fields():
                self.fields[field_name] = field

        # TODO: if ok to leave un-marshalled, then try to fullfill the promise when called?
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


class Base(object):
    """ Basic model for api items """

    Schema = None
    models = {}

    @validate_init
    def __init__(self, *args, **kwargs):
        vars(self).update(kwargs)
        self.raw = None
        self.__class__.check_for_schema()

    @classmethod
    def check_for_schema(cls):
        if not hasattr(cls, "Schema") or cls.Schema is None:
            raise MarshpillowError("Schema not found. @add_schema may not have been added to class definition.")

    def __getattr__(self, name, saveattr=False):
        # print("Getting {} from {}".format(name, self.__class__.__name__))
        if name not in vars(self):
            # print("{} not in object".format(name))
            if self._has_relationship(name):
                # print("fullfilling relationship...")
                v = self.fullfill_relationship(name)
                if saveattr:
                    setattr(self, name, v)
                return v
        v = super().__get_attribute__()
        if self._has_relationship(name):
            r = self._get_relationship(name)
            fxn = r._get_function()
            # TODO: Try to unmarshall if its something like "sequences": {"id"}
        return v

    def _has_relationship(self, name):
        return name in self.Schema.relationships

    @classmethod
    def model_fields(cls):
        members = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        return [m for m in members if issubclass(m[1].__class__, fields.Field)]

    def _get_relationship(self, name):
        return self.Schema.relationships[name]

    def fullfill_relationship(self, relationship_name):
        """
        Fullfills a relationship using "using", "ref", "fxn."

        Sample
            Promise("sample_type", <SampleType>, "sample_type_id", "find")
        """
        relationship = self._get_relationship(relationship_name)
        return relationship.fullfill(self)

    # def _parse_model_from_name(self, name):
    #     model_name = utils.snake_to_camel(name)
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
        model_name = utils.snake_to_camel(name)  # class name of the model to use
        model = cls.models[model_name]
        return model

    @classmethod
    def get_schema_opts(cls):
        if hasattr(cls, "SCHEMA_OPTS"):
            return cls.SCHEMA_OPTS
        else:
            return {}

    @classmethod
    def json_to_model(cls, result):
        m = cls.to_model(result)
        m.raw = result
        return m

    @classmethod
    def json_to_models(cls, result):
        m = cls.to_model(result, {"many": True})
        for r, model in zip(result, m):
            model.raw = r
        return m

    # def fullfill(self, name, relationship):
    #     if relationship.reference is None:
    #         # get from _id
    #         x = name+"_id"
    #         if hasattr(self, x):
    #             model_id = getattr(self, x)

    @classmethod
    def find(cls, id):
        raise NotImplementedError("method \"find\" is not yet implemented for {0}. Find returns a single model from an "
                                  "id.".format(cls.__name__))

    @classmethod
    def where(cls, *args, **kwargs):
        raise NotImplementedError("method \"where\" is not yet implemented for {0}. Where returns multiple models "
                                  "from a "
                                  "query.".format(cls.__name__))

    @classmethod
    def find_by_name(cls, name):
        raise NotImplementedError("method \"find_by_name\" is not yet implemented for {0}. Where returns a single "
                                  "model "
                                  "from a "
                                  "str.".format(cls.__name__))

    @classmethod
    def load(cls, data):
        """ Special load that will unmarshall dict objects or a list of dict objects """
        cls.check_for_schema()
        if type(data) is list:
            return cls.json_to_models(data)
        elif type(data) is dict:
            return cls.json_to_model(data)
        else:
            raise MarshpillowError("Data not recognized. Supply a dict or list: \"{0}\"".format(data))
