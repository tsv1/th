from unittest.mock import sentinel as s

from pytest import raises

from th import _, get


def test_resolve_class_attribute():
    class User:
        name = "Bob"

    assert get(User, _.name) == User.name


def test_resolve_nonexisting_class_attribute():
    class User:
        pass

    with raises(AttributeError):
        get(User, _.unknown)


def test_resolve_nonexisting_class_attribute_with_default():
    class User:
        pass

    assert get(User, _.unknown, default=s.default) == s.default


def test_resolve_public_instance_attribute():
    class User:
        def __init__(self, name):
            self.name = name

    user = User("Bob")
    assert get(user, _.name) == user.name


def test_resolve_protected_instance_attribute():
    class User:
        def __init__(self, name):
            self._name = name

    user = User("Bob")
    assert get(user, _._name) == user._name


def test_resolve_private_instance_attribute():
    class User:
        def __init__(self, name):
            self.__name = name

    user = User("Bob")
    with raises(AttributeError):
        get(user, _.__name)


def test_resolve_nonexisting_instance_attribute():
    class User:
        pass

    user = User()
    with raises(AttributeError):
        get(user, _.name)


def test_resolve_nonexisting_instance_attribute_with_default():
    class User:
        pass

    user = User()
    assert get(user, _.name, default=s.default) == s.default


def test_resolve_sequence_index():
    numbers = [1, 2, 3]
    assert get(numbers, _[0]) == numbers[0]


def test_resolve_sequence_outside_index():
    numbers = []
    with raises(IndexError):
        get(numbers, _[len(numbers) + 1])


def test_resolve_sequence_outside_index_with_default():
    assert get([], _[0], default=s.default) == s.default


def test_resolve_sequence_slice():
    numbers = [1, 2, 3]
    assert get(numbers, _[0:1]) == numbers[0:1]


def test_resolve_sequence_inappropriate_type():
    numbers = [1, 2, 3]
    with raises(TypeError):
        get(numbers, _["first"])


def test_resolve_mapping_str_key():
    numbers = {
        "id": 1,
    }
    assert get(numbers, _["id"]) == numbers["id"]


def test_resolve_mapping_int_key():
    numbers = {
        0: "zero",
    }
    assert get(numbers, _[0]) == numbers[0]


def test_resolve_mapping_nonexisting_key():
    numbers = {}
    with raises(KeyError):
        get(numbers, _["key"])


def test_resolve_mapping_nonexisting_key_with_default():
    assert get({}, _["key"], default=s.default) == s.default
