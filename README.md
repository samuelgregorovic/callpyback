<a id="readme-top"></a>  

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

- Support `on_call`, `on_success`, `on_failure` and `on_end` callbacks
- Option to specify default return from the decorated function
- Option to pass local scope variables of the decorated function to the `on_end` callback
- Option to specify exception classes to be expected and invoke `on_failure` callback
- Option to omit callbacks - default callback
- Option to omit callback's function parameters (specify only those which you need)
- Option to execute callbacks on the background (new thread) via `@background_callpyback` decorator

### Instalation
Package is currently available under the same name at [![PyPI version](https://badge.fury.io/py/callpyback.svg)](https://badge.fury.io/py/callpyback).

`pip install callpyback`

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Usage

#### 1. Decorating the function with ```CallPyBack``` class decorator with callback functions specified

```python

def on_success(func_result):
    print(f'Done with a result: {func_result}!')

def on_failure(func_exception):
    print(f'Failed with an error: {func_exception}!')


@CallPyBack(on_success=on_success, on_failure=on_failure)
def method()
    pass

method()
```

#### 2. Preconfigured ```CallPyBack``` callback custom class
```python

def on_success(func_result):
    print(f'Done with a result: {func_result}!')

def on_failure(func_exception):
    print(f'Failed with an error: {func_exception}!')

custom_callpyback = CallPyBack(
    on_success=on_success,
    on_failure=on_failure
)

@custom_callpyback
def method():
    pass

method()
```

#### 3. Using ```@background_callpyback``` decorator to make callback execute on the background thread
```python

@background_callpyback
def on_success(func_result):
    print(f'Done with a result: {func_result}!')

def on_failure(func_exception):
    print(f'Failed with an error: {func_exception}!')

custom_callpyback = CallPyBack(
    on_success=on_success,
    on_failure=on_failure
)

@custom_callpyback
def method():
    pass

method()
```
In this case, `on_success` will be executed on the background thread, while `on_failure` will be executed in a blocking way.


#### 4. Passing local variables of decorated function, specified in `pass_vars` to `on_end` callback
```python

def on_end(func_result, func_scope_vars):
    print(f'Done with a result: {func_result}!')
    print(f'Local function variables: {func_scope_vars}')

custom_callpyback = CallPyBack(
    on_end=on_end,
    pass_vars=('a', 'b')
)

@custom_callpyback
def method():
    a = 0
    b = 1
    return a

method()
```


#### 5. Specifiyng default return value by `default_return` parameter.
```python


custom_callpyback = CallPyBack(
    default_return=-1
)

@custom_callpyback
def method():
     raise KeyError('fail')

result = method()
```
In this case, result will be equal to `-1` specified in `default_return`.


#### 6. Specifiyng exception classes to be caught by `exception_classes` parameter.
```python

def on_failure(func_exception):
    print(f'Failed with an error: {func_exception}!')

custom_callpyback = CallPyBack(
    on_failure=on_failure,
    exception_classes=(TypeError,)
)

@custom_callpyback
def method():
     raise KeyError('fail')

result = method()
```
In this case, exception will be raised, which will not execute failure handler, but re-raise original exception.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Roadmap

- [x] Add Changelog
- [x] Support `on_call`, `on_success`, `on_failure` and `on_end` callbacks
- [x] Option to specify default return from the decorated function
- [x] Option to pass local scope variables of the decorated function to the `on_end` callback
- [x] Option to specify exception classes to be expected and invoke `on_failure` callback
- [x] Option to omit callbacks - default callback
- [x] Option to omit callback's function parameters (specify only those which you need)
- [x] Option to execute callbacks on the background (new thread) via `@background_callpyback` decorator
- [ ] Add `asyncio` support for decorated function
- [ ] Add `asyncio` support for callback function
- [ ] TBD...

See the [open issues](https://github.com/samuelgregorovic/callpyback/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/feature-name`)
3. Commit your Changes (`git commit -m 'Add some FeatureName'`)
4. Push to the Branch (`git push origin feature/feature-name`)
5. Open a Pull Request
6. Let us review your magical feature

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See [`LICENSE.txt`](https://github.com/samuelgregorovic/callpyback/blob/main/LICENSE.txt) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Samuel Gregorovič - [samuel-gregorovic](https://www.linkedin.com/in/samuel-gregorovic) - samuelgregorovic@gmail.com

Project Link: [https://github.com/samuelgregorovic/callpyback](https://github.com/samuelgregorovic/callpyback)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
