import pytest
from marshpillow import utils

def test_string_case():
    s1 = "ipsum"
    s2 = "carpe diem"
    s3 = "CarpeDiem"
    s4 = "carpe_diem"

    assert utils.is_snake(s1)
    assert not utils.is_snake(s2)
    assert not utils.is_snake(s3)
    assert utils.is_snake(s4)

    assert not utils.is_camel(s1)
    assert not utils.is_camel(s2)
    assert utils.is_camel(s3)
    assert not utils.is_camel(s4)

    assert utils.camel_to_snake(s3) == s4
    assert utils.snake_to_camel(s4) == s3