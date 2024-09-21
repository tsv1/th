# `th`

[![Codecov](https://img.shields.io/codecov/c/github/tsv1/th/master.svg?style=flat-square)](https://codecov.io/gh/tsv1/th)
[![PyPI](https://img.shields.io/pypi/v/th.svg?style=flat-square)](https://pypi.python.org/pypi/th/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/th?style=flat-square)](https://pypi.python.org/pypi/th/)
[![Python Version](https://img.shields.io/pypi/pyversions/th.svg?style=flat-square)](https://pypi.python.org/pypi/th/)

## Introduction

`th` is a Python library that provides a convenient way to access nested attributes and items in complex data structures, with clear and informative error messages when something goes wrong.

When working with deeply nested data structures like JSON responses or complex objects, accessing nested attributes or items can lead to confusing and uninformative error messages when a part of the path doesn't exist or is of the wrong type.

`th` simplifies this by allowing you to specify the path using a special path holder object `_`, and provides detailed error messages indicating exactly where the problem occurred.

## Installation

You can install `th` using pip:

```sh
pip install th
```

## Usage

### Basic Usage

Suppose you have a complex `response` object and you want to access a nested value:

```python
username = response.body["users"][0]["name"]
```

If any part of this path doesn't exist or is `None`, you might get a `TypeError` or `AttributeError` with a less-than-helpful message.

With `th`, you can do:

```python
from th import get, _

username = get(response, _.body["users"][0]["name"])
```

If everything goes well, `username` will be set to the desired value. If there's an error, `th` will raise an informative exception showing exactly where the problem occurred in the path.

### Providing a Default Value

If you want to provide a default value in case the path doesn't exist or is of the wrong type, you can use the `default` parameter:

```python
username = get(response, _.body["users"][0]["name"], default="Unknown")
```

If one of the parts of the path doesn't exist or is of the wrong type, `username` will be set to "Unknown".

### Verbose Mode

If you need more detailed information about the error, you can enable verbose mode:

```python
username = get(response, _.body["users"][0]["name"], verbose=True)
```

Suppose `response.body["users"]` is `None`, you would get an error message like:

```
th.TypeError: _.body['users'][0]['name']
              ^^^^^^^^^^^^^^^ inappropriate type (NoneType)
where _ is <class 'Response'>:
Response({'total': 3, 'users': None})
```

This includes additional debug information in the error message, such as the type and value of the object at the point of failure.
