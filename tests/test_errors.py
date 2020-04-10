from traceback import format_exception

from pytest import raises

import th
from th import _, get


def test_attribute_error():
    exception = "th.AttributeError: _.body['items'][0]\n" \
                "                     ^^^^ does not exist"

    with raises(th.AttributeError) as exc:
        get(None, _.body["items"][0])

    tb = "".join(format_exception(exc.type, exc.value, exc.tb))
    assert tb.endswith(exception + "\n")

    assert repr(exc.value) == exception


def test_index_error():
    exception = "th.IndexError: _['items'][10]\n" \
                "                          ^^ out of range"

    with raises(th.IndexError) as exc:
        get({"items": [1, 2, 3]}, _["items"][10])

    tb = "".join(format_exception(exc.type, exc.value, exc.tb))
    assert tb.endswith(exception + "\n")

    assert repr(exc.value) == exception


def test_key_error():
    exception = "th.KeyError: _['result']['items']\n" \
                "                         ^^^^^^^ does not exist"

    with raises(th.KeyError) as exc:
        get({"result": {}}, _["result"]["items"])

    tb = "".join(format_exception(exc.type, exc.value, exc.tb))
    assert tb.endswith(exception + "\n")

    assert repr(exc.value) == exception


def test_type_error():
    exception = "th.TypeError: _['status'][None]\n" \
                "                          ^^^^ inappropriate type (NoneType)"

    with raises(th.TypeError) as exc:
        get({"status": "OK"}, _["status"][None])

    tb = "".join(format_exception(exc.type, exc.value, exc.tb))
    assert tb.endswith(exception + "\n")

    assert repr(exc.value) == exception


def test_type_error_subscriptable():
    exception = "th.TypeError: _['status'][0]\n" \
                "              ^^^^^^^^^^^ inappropriate type (int)"

    with raises(th.TypeError) as exc:
        get({"status": 200}, _["status"][0])

    tb = "".join(format_exception(exc.type, exc.value, exc.tb))
    assert tb.endswith(exception + "\n")

    assert repr(exc.value) == exception
