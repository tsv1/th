from th.operators import AttrAccessor, ItemAccessor


def test_item_accessor():
    target = {"key": "val"}
    accessor = ItemAccessor("key")

    assert accessor(target) == target["key"]


def test_item_accessor_eq():
    assert ItemAccessor("key") == ItemAccessor("key")
    assert ItemAccessor("key") != ItemAccessor("another_key")


def test_item_accessor_str():
    accessor = ItemAccessor("key")
    assert str(accessor) == "['key']"


def test_item_accessor_repr():
    accessor = ItemAccessor("key")
    assert repr(accessor) == "ItemAccessor('key')"


def test_attr_accessor():
    class User:
        name = "<name>"

    accessor = AttrAccessor("name")
    assert accessor(User) == "<name>"


def test_attr_accessor_eq():
    assert AttrAccessor("attr") == AttrAccessor("attr")
    assert AttrAccessor("attr") != AttrAccessor("another_attr")


def test_atr_accessor_str():
    accessor = AttrAccessor("attr")
    assert str(accessor) == ".attr"


def test_atr_accessor_repr():
    accessor = AttrAccessor("attr")
    assert repr(accessor) == "AttrAccessor('attr')"
