from schema import add_schema
from pillowtalkbase import PillowtalkBase


def test_dump():
    """Test loading a model with ignored fields. The model is expected to NOT have an id or field1, but
    have a name"""

    @add_schema
    class MyModel(PillowtalkBase):
        class Fields:
            load_all = True


    original_data = {"id": 5, "name": "Jill", "field1": 1}
    u = MyModel.load(original_data)

    assert u.id == 5
    assert u.field1 == 1
    assert u.name == "Jill"

    d = u.dump()
    assert d == original_data


def test_load_only():
    """Test loading a model with ignored fields. The model is expected to NOT have an id or field1, but
    have a name"""

    @add_schema
    class MyModel(PillowtalkBase):
        class Fields:
            load_all = True
            load_only = ("name",)

    original_data = {"id": 5, "name": "Jill", "field1": 1}
    u = MyModel.load(original_data)

    assert u.id == 5
    assert u.field1 == 1
    assert u.name == "Jill"

    d = u.dump()
    assert d == {"id": 5, "field1": 1}


def test_load_dump_repeat():
    """Test loading a model with ignored fields. The model is expected to NOT have an id or field1, but
    have a name"""

    @add_schema
    class MyModel(PillowtalkBase):
        class Fields:
            load_all = True

    original_data = {"id": 5, "name": "Jill", "field1": 1}

    ## load/dump cycle 1

    # check load
    u = MyModel.load(original_data)
    assert u.id == 5
    assert u.field1 == 1
    assert u.name == "Jill"

    # check dump
    d = u.dump()
    assert d == original_data

    # check instance again
    assert u.id == 5
    assert u.field1 == 1
    assert u.name == "Jill"


    ## load/dump cycle 2

    # check load
    u = MyModel.load(original_data)
    assert u.id == 5
    assert u.field1 == 1
    assert u.name == "Jill"

    # check dump
    d = u.dump()
    assert d == original_data

    # check instance again
    assert u.id == 5
    assert u.field1 == 1
    assert u.name == "Jill"
