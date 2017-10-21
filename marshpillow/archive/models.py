from marshpillow import *
from marshpillow import validate_init
from marshpillow.schemas import add_schema


class AqBase(MarshpillowBase):
    """ Basic model for api items """

    Schema = None
    models = {}

    @validate_init
    def __init__(self, *args, **kwargs):
        vars(self).update(kwargs)

    def __getattr__(self, name):
        if name in vars(self):
            return getattr(self, name)
        elif name+"_id" in vars(self):
            return self._parse_model_from_name(name)

    def _parse_model_from_name(self, name):
        model_name = utils.snake_to_camel(name)
        model = MarshpillowBase.models[model_name]
        model_id = getattr(self, name+"_id")
        m = model.find(model_id)
        setattr(self, name, m)
        return m

    @classmethod
    def _post_json(cls, data, as_json=False):
        d = {'model': cls.__name__}
        d.update(data)
        r = Session.session._post('json', json=d).json()
        if not as_json:
            r = cls.to_model(r)
        return r

    @classmethod
    def to_model(cls, result):
        schema = cls.Schema()
        model, errors = schema.load(result)
        return model

    @classmethod
    def to_models(cls, result):
        schema = cls.Schema(many=True)
        model, errors = schema.load(result)
        return model

    @classmethod
    def find(cls, id, as_json=False):
        return cls._post_json({"id": id}, as_json=as_json)

    @classmethod
    def find_by_name(cls, name, as_json=False):
        return cls._post_json({"method": "find_by_name", "arguments": [name]}, as_json=as_json)

    @classmethod
    def array_query(cls, method, args, rest, opts={}, as_json=False):
        options = {"offset": -1, "limit": -1, "reverse": False}
        options.update(opts)
        query = {"model"    : cls.__name__,
                 "method"   : method,
                 "arguments": args,
                 "options"  : options}
        query.update(rest)
        r = cls._post_json(query)
        if "errors" in r:
            raise Exception(cls.__name__+": "+r["errors"])
        if not as_json:
            r = cls.to_models(r)
        return r

    @classmethod
    def all(cls, rest={}, opts={}, as_json=False):
        options = {"offset": -1, "limit": -1, "reverse": False}
        options.update(opts)
        return cls.array_query("all", [], rest, options, as_json=as_json)

    @classmethod
    def where(cls, criteria, methods={}, opts={}, as_json=False):
        options = {"offset": -1, "limit": -1, "reverse": False}
        options.update(opts)
        return cls.array_query("where", criteria, methods, options, as_json=as_json)


@add_schema
class Sample(AqBase):
    FIELDS = ["name", "id", "project", "description", "sample_type_id", "user_id"]
    ONE = [
        ("sample_type", {"using": "sample_type_id", "with": "find"}),
        ("user", {"using": "user_id", "with": "find"})
    ]
    ALLOW_NONE = ["description"]

@add_schema
class SampleType(AqBase):
    FIELDS = ["name", "id"]

@add_schema
class User(AqBase):
    FIELDS = ["name", "id"]


Session._create_with_connector(,,, "vrana", "Mountain5", "http://52.27.43.242:81/"

s = Sample.find(1111)
print(s)
print(s.sample_type)
print(s.user)