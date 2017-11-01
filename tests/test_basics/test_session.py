import pytest
import os
from pillowtalk import *
import copy

@pytest.fixture
def APIs():
    class API1(object):
        def __init__(self, login, password, home):
            vars(self).update(locals())

    class API2(object):
        def __init__(self, login, password, home):
            vars(self).update(locals())

    class MySession(SessionManager):

        pass

    return API1, API2, MySession


def test_create_sessions(APIs):
    API1, API2, Session = APIs

    cred1 = {"login": "John", "password": "Thomason", "home": "www.johnnyt.com"}

    cred2 = {"login": "John", "password": "Flompson", "home": "www.johnnyf.com"}

    Session().register_connector(API1(**cred1), session_name="API1")
    Session().register_connector(API2(**cred2), session_name="API2")

    api1 = Session().API1
    assert Session().session is not None
    api2 = Session().API2
    assert Session().session is not None

    assert api1.__dict__ != api2.__dict__
    assert api1.password == cred1["password"]
    assert api2.password == cred2["password"]


def test_raise_attribute_error():

    s = SessionManager()
    with pytest.raises(AttributeError):
        s.name

def test_create_sessions(APIs):
    s = SessionManager()
    s.name = "before"
    this_dir = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.dirname(this_dir)
    file = os.path.join(test_dir, 'pickle_tests', 'pickle1.pkl')
    s.save(file)
    s.name = "after"
    assert SessionManager().name == "after"
    s.load(file)
    assert SessionManager().name == "before"