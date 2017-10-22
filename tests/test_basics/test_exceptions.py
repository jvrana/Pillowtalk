import pytest

from pillowtalk import PillowtalkError


def test_exception(mybase):

    class Person(mybase):
        FIELDS = ["id", "name"]

    with pytest.raises(PillowtalkError):
        Person.load({"id": 5, "name": "Opps"})