# callpyback
[![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue.svg)](https://python.org)
[![Build Status](https://github.com/samuelgregorovic/callpyback/actions/workflows/build.yaml/badge.svg)](https://github.com/samuelgregorovic/callpyback/actions/workflows/build.yaml)
[![Coverage Status](https://coveralls.io/repos/github/samuelgregorovic/callpyback/badge.svg)](https://coveralls.io/github/samuelgregorovic/callpyback)
[![PyPI version](https://badge.fury.io/py/callpyback.svg)](https://badge.fury.io/py/callpyback)
[![Known Vulnerabilities](https://snyk.io/test/github/samuelgregorovic/callpyback/badge.svg)](https://snyk.io/test/github/samuelgregorovic/callpyback)
[![Maintainability](https://api.codeclimate.com/v1/badges/6473b57bc8600e5ad6f6/maintainability)](https://codeclimate.com/github/samuelgregorovic/callpyback/maintainability)
[![Issues](https://img.shields.io/github/issues/samuelgregorovic/callpyback.svg?maxAge=2592000)](https://github.com/samuelgregorovic/callpyback/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![ Repo Size](https://img.shields.io/github/repo-size/samuelgregorovic/callpyback)
[![Downloads](https://static.pepy.tech/badge/callpyback)](https://pepy.tech/project/callpyback)
[![Project Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Commit activity](https://img.shields.io/github/commit-activity/m/samuelgregorovic/callpyback)](https://github.com/samuelgregorovic/callpyback/pulse)

## Features

- on_call callback
- on_success callback
- on_failure callback
- on_end callback
- default return
- using local variables of function in on_end
- support for async/sync callbacks with auto-detect
- support for omitting callback functions parameters with auto-detect
- pre-defining custom callback with creating class instance and using it as decorator
- TBD

### Instalation
`pip install callpyback`

### Usage

#### 1. ```CallPyBack``` callback class
```python
@CallPyBack(on_success=func_on_success, on_fail=func_on_fail, on_end=func_on_end)
def method()
    pass

method()
```
Will produce the same results as `callpyback` decorator. Can be extended further.

#### 2. Preconfigured ```CallPyBack``` callback custom class
```python
custom_callpyback = CallPyBack(
    on_success=func_on_success, on_fail=func_on_fail, on_end=func_on_end
)

@custom_callpyback
def method():
    pass

method()
```
Will produce the same results as `callpyback` decorator and `CallPyBack` class. Can be preconfigured to use specific callback functions with initiating a `CallPyBack` class instance.
