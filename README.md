# th

## Overview

```python
username = response.body["users"][0]["name"]

TypeError: 'NoneType' object is not subscriptable
```

becomes:

```python
from th import get, _
username = get(response, _.body["users"][0]["name"])

th.TypeError: _.body['users'][0]['name']
              ^^^^^^^^^^^^^^^ inappropriate type (NoneType)
```

## Installation

```sh
pip3 install th
```

## Usage

#### Default

```python
total = get(response, _.body["total"], default=0)
# no exception
```

#### Verbose

```python
user = get(response.body, _["users"][4]["id"], verbose=True)

th.IndexError: _['users'][4]['id']
                          ^ out of range
where _ is <class 'dict'>:
{'users': [{'id': 1, 'name': 'Bob'},
           {'id': 2, 'name': 'Alice'},
           {'id': 3, 'name': 'Eve'}]}
```

## Examples

```python
AttributeError: 'Response' object has no attribute 'body'
# ->
th.AttributeError: _.body['users'][0]['name']
                     ^^^^ does not exist
```
```python
IndexError: list index out of range
# ->
th.IndexError: _.body['users'][0]['name']
                               ^ out of range
```
```python
KeyError: 'users'
# ->
th.KeyError: _.body['users'][0]['name']
                    ^^^^^^^ does not exist
```
```python
TypeError: list indices must be integers or slices, not NoneType
# -> 
th.TypeError: _.body['users'][None]['name']
                              ^^^^ inappropriate type (NoneType)
```
```python
TypeError: 'NoneType' object is not subscriptable
# ->
th.TypeError: _.body['users'][0]['name']
              ^^^^^^^^^^^^^^^ inappropriate type (NoneType)
```
