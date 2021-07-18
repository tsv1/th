from copy import copy, deepcopy
from typing import Generator

import pytest

from th import PathHolder, PathHolderProxy


@pytest.fixture()
def proxy() -> PathHolderProxy:
    return PathHolderProxy(PathHolder)


def test_path_holder_proxy_repr(*, proxy: PathHolderProxy):
    assert repr(proxy) == f"PathHolderProxy({PathHolder!r})"


def test_path_holder_eq():
    assert PathHolderProxy(PathHolder) == PathHolderProxy(PathHolder)
    assert PathHolderProxy(PathHolder) != PathHolderProxy(lambda: PathHolder())


def test_path_holder_proxy_copy(*, proxy: PathHolderProxy):
    copied = copy(proxy)
    assert copied == proxy
    assert id(copied) != id(proxy)


def test_path_holder_proxy_deepcopy(*, proxy: PathHolderProxy):
    copied = deepcopy(proxy)
    assert copied == proxy
    assert id(copied) != id(proxy)


def test_path_holder_proxy_len(*, proxy: PathHolderProxy):
    assert len(proxy) == 0


def test_path_holder_proxy_iter(*, proxy: PathHolderProxy):
    assert isinstance(iter(proxy), Generator)

    assert list(x for x in proxy) == []
