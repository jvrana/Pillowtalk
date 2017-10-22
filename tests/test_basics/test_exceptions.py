import pytest

from pillowtalk import MarshpillowError


def test_exception(mybase):

    class Person(mybase):
        FIELDS = ["id", "name"]

    with pytest.raises(MarshpillowError):
        Person.load({"id": 5, "name": "Opps"})