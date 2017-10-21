import pytest

from marshpillow import *


@pytest.fixture
def APIs():
    class API1(SessionManager):
        def __init__(self, login, password, home):
            vars(self).update(locals())

    class API2(SessionManager):
        def __init__(self, login, password, home):
            vars(self).update(locals())

    return API1, API2


def test_create_sessions(APIs):
    API1, API2 = APIs

    cred1 = {"login": "John", "password": "Thomason", "home": "www.johnnyt.com"}

    cred2 = {"login": "John", "password": "Flompson", "home": "www.johnnyf.com"}

    API1.create(**cred1)

    API2.create(**cred2)

    assert API1.session is not None
    assert API2.session is not None
    assert API1.session.__dict__ != API2.session.__dict__
    assert API1.session.password == cred1["password"]
    assert API2.session.password == cred2["password"]
