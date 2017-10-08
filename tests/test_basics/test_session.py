import pytest
from marshpillow import *

@pytest.fixture
def API():
    class API(object):

        def __init__(self, login, password, home):
            vars(self).update(locals())
    return API

@pytest.fixture
def fastfoodexample(API):
    credential_list = [
        {
            "login"   : "TimHorton",
            "password": "mmmmmmDonuts",
            "home"    : "www.timmyhortons.eh/sorry",
            "name": "CANADA"
        },
        {
            "login"   : "Wendy",
            "password": "burgers",
            "home"    : "www.WendysFries.com",
            "name": "USA"
        }
    ]

    for cred in credential_list:
        SessionManager.create(API, **cred)
    return credential_list

def test_session_creator(API):
    credentials = {
        "login": "TimHorton",
        "password": "mmmmmmDonuts",
        "home": "www.timmyhortons.can"
    }

    SessionManager.create(API, **credentials)
    s = SessionManager.session
    assert type(s) is API
    for k, v in credentials.items():
        assert getattr(SessionManager.session, k) == v

def test_session_set(fastfoodexample):
    credential_list = fastfoodexample
    for cred in credential_list:
        SessionManager.set(cred["name"])
        assert SessionManager.session_name() == cred["name"]
        for k, v in cred.items():
            if k != "name":
                assert getattr(SessionManager.session, k) == v

def test_session_hook(fastfoodexample):
    credential_list = fastfoodexample
    for cred in credential_list:
        getattr(SessionManager, cred["name"])
        for k, v in cred.items():
            if k != "name":
                assert getattr(SessionManager.session, k) == v

def test_session_close(fastfoodexample):
    SessionManager.close()
    assert SessionManager.session is None

