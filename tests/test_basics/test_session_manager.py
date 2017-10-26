import pytest
from pillowtalk import *

@pytest.fixture
def API():
    class API(object):

        def __init__(self, login, password, home, session_name=None):
            vars(self).update(locals())
    return API

@pytest.fixture
def fastfoodexample(API):
    credential_list = [
        {
            "login"   : "TimHorton",
            "password": "mmmmmmDonuts",
            "home"    : "www.timmyhortons.eh/sorry",
            "session_name": "CANADA"
        },
        {
            "login"   : "Wendy",
            "password": "burgers",
            "home"    : "www.WendysFries.com",
            "session_name": "USA"
        }
    ]

    for cred in credential_list:
        SessionManager.register_connector(API(**cred), cred["session_name"])
    return credential_list

def test_session_subclass(API):
    credential_list = [
        {
            "login"   : "McDonalds",
            "password": "lsdlfasdjf",
            "home"    : "www.dfsfs.eh/sorry",
            "session_name"    : "USA"
        },
    ]

    class Session(SessionManager):

        @classmethod
        def create(cls, session_name=None, **cred):
            return cls.register_connector(API(**cred), session_name=session_name)

    for cred in credential_list:
        Session.create(**cred)

    assert Session.session is not None


def test_session_creator(API):
    credentials = {
        "login": "TimHorton",
        "password": "mmmmmmDonuts",
        "home": "www.timmyhortons.can"
    }

    SessionManager.register_connector(API(**credentials))
    s = SessionManager.session
    assert type(s) is API
    for k, v in credentials.items():
        assert getattr(SessionManager.session, k) == v

def test_session_set(fastfoodexample):
    assert SessionManager.session is not None

def test_session_set(fastfoodexample):
    credential_list = fastfoodexample
    for cred in credential_list:
        SessionManager.set(cred["session_name"])
        assert SessionManager.session_name == cred["session_name"]
        for k, v in cred.items():
            if k != "session_name":
                assert getattr(SessionManager.session, k) == v

def test_session_hook(fastfoodexample):
    credential_list = fastfoodexample
    for cred in credential_list:
        getattr(SessionManager, cred["session_name"])
        for k, v in cred.items():
            if k != "session_name":
                assert getattr(SessionManager.session, k) == v

def test_session_close(fastfoodexample):
    assert SessionManager.session is not None
    SessionManager.close()
    assert SessionManager.session is None

def test_multiple_session_classes(fastfoodexample):

    class NewSession(SessionManager):
        pass

    assert NewSession.session is None

def test_session_reset(fastfoodexample):
    assert SessionManager.session is not None
    SessionManager.reset()
    assert SessionManager.empty()
    assert SessionManager.session is None

def test_session_exceptions(fastfoodexample):
    SessionManager.sessions = None
    with pytest.raises(PillowtalkSessionError):
        SessionManager.set("something")

    SessionManager.sessions = {}
    with pytest.raises(PillowtalkSessionError):
        SessionManager.set("something")

def test_session_registration_after_sessions_is_None(API):
    SessionManager.reset()
    SessionManager.sessions = None
    credentials = {
        "login": "TimHorton",
        "password": "mmmmmmDonuts",
        "home": "www.timmyhortons.can"
    }

    SessionManager.register_connector(API(**credentials))
