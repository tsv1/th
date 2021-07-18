from copy import copy, deepcopy

from th import _


def test_holder_mutable():
    holder = _.items
    holder[0]
    holder["id"]

    assert repr(holder) == "_.items[0]['id']"


def test_holder_repr_index():
    assert repr(_[0]) == "_[0]"


def test_holder_repr_key():
    assert repr(_["id"]) == "_['id']"


def test_holder_repr_attr():
    assert repr(_.name) == "_.name"


def test_holder_repr_custom():
    class Key:
        def __repr__(self):
            return "<Key>"

    assert repr(_[Key()]) == "_[<Key>]"


def test_holder_repr_nested():
    nested = _.items[0]["id"]
    assert repr(nested) == "_.items[0]['id']"


def test_holder_eq():
    assert _ == _
    assert _.items[0].name == _.items[0].name
    assert _.items[0].name != _.items[0].name1
    assert _.items[0].name != _.items[1].name


def test_holder_copy():
    holder1 = _.items[0].name
    holder2 = copy(holder1)

    assert holder1 == holder2
    assert id(holder1) != id(holder2)


def test_holder_copy_and_update():
    holder1 = _.items[0]
    holder2 = copy(holder1).name

    assert holder1 == holder2 == _.items[0].name


def test_holder_deepcopy():
    holder1 = _.items[0].name
    holder2 = deepcopy(holder1)

    assert holder1 == holder2
    assert id(holder1) != id(holder2)


def test_holder_deepcopy_and_update():
    holder1 = _.items[0]
    holder2 = deepcopy(holder1).name

    assert holder1 != holder2
    assert holder1 == _.items[0]
    assert holder2 == _.items[0].name


def test_holder_len():
    holder = _.items[0].name

    assert len(holder) == 3
