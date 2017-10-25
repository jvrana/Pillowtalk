# TODO: Make session a dict of class names and session...
# TODO: Make sessions a dict of dict of classname and sessions
# TODO: Test to make sure session and sessions aren't shared between Subclasses


class SessionManagerHook(type):
    #
    def __init__(cls, name, bases, clsdict):
        cls.session = None
        cls.sessions = {}
        super(SessionManagerHook, cls).__init__(name, bases, clsdict)

    def __getattr__(cls, item):
        sessions = object.__getattribute__(cls, "sessions")
        if item in sessions:
            cls.set(item)
        else:
            try:
                return object.__getattribute__(cls, item)
            except AttributeError:
                msg = "Attribute \"{0}\" not found.".format(item)
                if sessions is None or sessions == []:
                    msg += " There are no sessions available."
                else:
                    msg += " Available sessions: {0}.".format(sessions.keys())
                raise AttributeError(msg)


class SessionManager(object, metaclass=SessionManagerHook):
    """ Session manager """

    session = None
    sessions = {}

    @classmethod
    def register_connector(cls, api_connector_instance, session_name=None):
        cls.session = api_connector_instance
        cls._add_session(cls.session, session_name)
        cls.set(session_name)

    @classmethod
    def _add_session(cls, api_connector, name):
        cls.sessions[name] = api_connector

    @classmethod
    def set(cls, name):
        cls.session = cls.sessions[name]

    @classmethod
    def session_name(cls):
        for name, session in cls.sessions.items():
            if cls.session == session:
                return name

    @classmethod
    def close(cls):
        cls.session = None

    @classmethod
    def reset(cls):
        cls.sessions = None
        cls.session = None


