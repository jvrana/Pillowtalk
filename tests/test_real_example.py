import os
import requests
from marshpillow import *
from marshmallow import pprint

def test_benchling_example():
    class BenchlingAPIException(Exception):
        """Generic Exception for BenchlingAPI"""


    class BenchlingLoginError(Exception):
        """Errors for incorrect login credentials"""


    class RequestDecorator(object):
        """
        Wraps a function to raise error with unexpected request status codes
        """

        def __init__(self, status_codes):
            if not isinstance(status_codes, list):
                status_codes = [status_codes]
            self.code = status_codes

        def __call__(self, f):
            def wrapped_f(*args, **kwargs):
                args = list(args)
                args[1] = os.path.join(args[0].home, args[1])
                r = f(*args)
                if r.status_code not in self.code:
                    http_codes = {
                        403: "FORBIDDEN",
                        404: "NOT FOUND",
                        500: "INTERNAL SERVER ERROR",
                        503: "SERVICE UNAVAILABLE",
                        504: "SERVER TIMEOUT"}
                    msg = ""
                    if r.status_code in http_codes:
                        msg = http_codes[r.status_code]
                    raise BenchlingAPIException("HTTP Response Failed {} {} {}, {}".format(
                            r.status_code, msg, args, kwargs))
                return r.json()

            return wrapped_f

    # Benchling API Info: https://api.benchling.com/docs/#sequence-sequence-collections-post
    class BenchlingAPI(object):
        """
        Connects to BenchlingAPI
        """

        # TODO: Create SQLite Database for sequences
        def __init__(self, api_key, home='https://api.benchling.com/v1/'):
            """
            Connects to Benchling

            :param api_key: api key
            :type api_key: str
            :param home: url
            :type home: str
            """
            self.home = home
            self.auth = (api_key, '')

        def update(self):
            """
            Updates the api cache

            :return: None
            :rtype: None
            """
            self._update_dictionaries()

        @RequestDecorator([200, 201, 202])
        def _post(self, what, data):
            return requests.post(what, json=data, auth=self.auth)

        @RequestDecorator([200, 201])
        def _patch(self, what, data):
            return requests.patch(what, json=data, auth=self.auth)

        @RequestDecorator(200)
        def _get(self, what, data=None):
            if data is None:
                data = {}
            print(what)
            print(data)
            print(self.auth)
            return requests.get(what, json=data, auth=self.auth)

        @RequestDecorator(200)
        def _delete(self, what):
            return requests.delete(what, auth=self.auth)

    class Session:
        """ Creates api sessions """
        session = None
        login = None
        password = None
        url = None

        @classmethod
        def create(cls, key):
            cls.key = key
            cls.new()

        @classmethod
        def new(cls):
            cls.session = BenchlingAPI(cls.key)


    Session.create("sk_GbNYfhnukDU30J5fAebIjEj0d4YlJ")

    class MyBase(MarshpillowBase):

        items = {}

        @classmethod
        def pluralize(cls):
            return cls.__name__.lower()+"s"

        @classmethod
        def all(cls):
            r = Session.session._get(cls.pluralize())
            items = cls.load(r[cls.pluralize()])
            for i in items:
                cls.items[getattr(i, "id")] = i
            return items

        @classmethod
        def find(cls, id):
            r = Session.session._get(cls.pluralize() + "/{}".format(id))
            return cls.load(r)

        @classmethod
        def where(cls, data):
            found = []
            for item_key, item in cls.items.items():
                passed = True
                for data_key, data_val in data.items():
                    item_val = getattr(item, data_key)
                    if item_val != data_val:
                        passed = False
                if passed:
                    found.append(item)
            return found

    @add_schema
    class Folder(MyBase):
        items = {}

        # Requir
        FIELDS = ["id", "name"]
        RELATIONSHIPS = [
            Many("sequences", "where Folder.id <> Sequence.folder")
        ]

    @add_schema
    class Sequence(MyBase):
        items = {}
        FIELDS = ["id", "name"]
        RELATIONSHIPS = [
            One("folder", "find Sequence.folder <> Folder.id")
        ]

    # f = Folder.find('lib_pP6d50rJn1')
    # s = Sequence.find("seq_5AXMlSvB")
    # print(s)
    #
    # print("Sequences")
    # print(f.sequences)
    #
    # print("Folder")
    # print(s.folder)

    f = Folder.find('lib_7SuYiCxO')
    assert len(f.sequences) == len(f.raw["sequences"])
    s = Sequence.Schema()
    assert type(f.sequences[1]) is Sequence
    print(f.sequences[1].folder)
    # assert f.sequences[1].folder == f