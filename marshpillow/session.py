class SessionInterface(object):
    session = None
    session_dict = {}

    @classmethod
    def __getattr__(cls, name):
        return cls[name]

    @classmethod
    def __getitem__(cls, name):
        return cls.session_dict[name]

    @classmethod
    def create(cls, key):
        raise NotImplementedError("{0}.create has not yet been implemented.".format(cls.__name__))

    @classmethod
    def new(cls):
        raise NotImplementedError("{0}.new has not been implemented".format(cls.__name__))

class Session(SessionInterface):

    def __init__(self, *args, **kwargs):
        vars(self).update(locals())

    @classmethod
    def create(cls, key, name):

