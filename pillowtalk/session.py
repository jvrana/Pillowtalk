# TODO: Make session a dict of class names and session...
# TODO: Make sessions a dict of dict of classname and sessions
# TODO: Test to make sure session and sessions aren't shared between Subclasses
from .exceptions import PillowtalkSessionError
import dill

class SessionManagerHook(type):

    def __init__(cls, name, bases, selfdict):
        cls._shared_state = {}
        super(SessionManagerHook, cls).__init__(name, bases, selfdict)

    # def __getattr__(self, item):
    #     sessions = object.__getattribute__(self, "sessions")
    #     if item in sessions:
    #         self.set(item)
    #     else:
    #         try:
    #             return object.__getattribute__(self, item)
    #         except AttributeError:
    #             msg = "Attribute \"{0}\" not found.".format(item)
    #             if sessions is None or sessions == []:
    #                 msg += " There are no sessions available."
    #             else:
    #                 msg += " Available sessions: {0}.".format(list(sessions.keys()))
    #             raise AttributeError(msg)

    # @property
    # def session_name(self):
    #     for name, session in self.sessions.items():
    #         if self.session == session:
    #             return name


class SessionManager(object, metaclass=SessionManagerHook):
    """ Session manager """

    def __init__(self):
        shared_state = self.__class__._shared_state
        self.__dict__ = shared_state
        if shared_state == {}:
            self.session = None
            self.sessions = {}

    @property
    def session_name(self):
        for name, session in self.sessions.items():
            if self.session == session:
                return name

    def register_connector(self, api_connector_instance, session_name=None):
        """ registers an api_connector instance with session_name """
        self.session = api_connector_instance
        self._add_session(self.session, session_name)
        self.set(session_name)

    def _add_session(self, api_connector, name):
        if self.sessions is None:
            self.sessions = {}
        self.sessions[name] = api_connector

    def set(self, name):
        """ set session by name """
        if self.sessions is None:
            raise PillowtalkSessionError("No sessions found.")
        if name not in self.sessions:
            raise PillowtalkSessionError(
                    "Session named {} not found. Choose from {}".format(name, list(self.sessions.keys())))
        self.session = self.sessions[name]

    def empty(self):
        """ Checks if sessions is empty or None """
        return self.sessions is None or self.sessions == {}

    def close(self):
        """ closes the current session """
        self.session = None

    def reset(self):
        """ resets the sessions and current session """
        self.sessions = {}
        self.session = None

    def __getattr__(self, item):
        sessions = object.__getattribute__(self, "sessions")
        if item in sessions:
            self.set(item)
            return self.session
        else:
            try:
                return object.__getattribute__(self, item)
            except AttributeError:
                msg = "Attribute \"{0}\" not found.".format(item)
                if sessions is None or sessions == []:
                    msg += " There are no sessions available."
                else:
                    msg += " Available sessions: {0}.".format(list(sessions.keys()))
                raise AttributeError(msg)

    def save(self, filepath):
        with open(filepath, 'wb') as f:
            dill.dump(self, f)

    def load(self, filepath):
        with open(filepath, 'rb') as f:
            dill.load(f)

    def __setstate__(self, state):
        """ Override so that sessions can be updated with pickle.load """
        self.__class__._shared_state.update(state)
        self.__dict__ = self.__class__._shared_state
