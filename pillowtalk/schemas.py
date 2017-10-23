import inflection
from marshmallow import SchemaOpts, Schema, fields, post_load
from pillowtalk.base import PillowtalkBase
from pillowtalk.relationship import Relationship
from pillowtalk.exceptions import PillowtalkInitializerError


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
    PillowtalkBase.models[cls.__name__] = cls

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
            if hasattr(cls, Relationship.RELATIONSHIP_FIELD_NAME):
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
            except PillowtalkInitializerError as e:
                pass

    # end of ModeSchema

    cls.Schema = ModSchema
    return cls