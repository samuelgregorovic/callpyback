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

## Description
"callpyback" is a comprehensive Python library designed to help developers add callbacks to their functions with ease. It comes with a range of powerful features that make it easy to customize the behavior of your functions in different stages of their execution. 

You can specify callbacks for on_call, on_success, on_failure, and on_end, and customize the default return value from the decorated function. Additionally, you can pass local scope variables of the decorated function to the on_end callback and define expected exceptions to trigger the on_failure callback. If desired, you can also omit callbacks, falling back to default behavior, and choose which parameters of the callback function to use. Furthermore, with the @background_callback decorator, you can execute callbacks on the background, making it easier to manage concurrency in your code.

## Features

- Support `on_call`, `on_success`, `on_failure` and `on_end` callbacks
- Pass decorated function **kwargs and function itself to callbacks
- Option to specify default return from the decorated function
- Option to pass local scope variables of the decorated function to the `on_end` callback
- Option to specify exception classes to be expected and invoke `on_failure` callback
- Option to omit callbacks - default callback
- Option to omit callback's function parameters (specify only those which you need)
- Option to execute callbacks on the background (new thread) via `@background_callpyback` decorator

## Use cases
The "callpyback" library can be useful in a variety of real-world scenarios where you need to add custom behavior to your functions at different stages of their execution. For example:
- Debugging and logging: By using the `on_call`, `on_success`, `on_failure`, and `on_end` callbacks, you can print out messages to help you understand what's happening during the execution of your functions, for example, you may have a function that performs a database operation and you want to log each time the function is called, its parameters, and if it is successful or not. 
- Monitoring and alerting: By using the "on_success" and "on_failure" callbacks, you can set up custom alerts to notify you when a function has completed successfully or when it has failed.
- Error handling: By using the "on_failure" callback, you can specify how to handle exceptions raised by your functions and take appropriate actions, such as retrying the function or logging the error message.
- Background processing: By using the "@background_callback" decorator, you can execute your callbacks on a separate thread, which can be useful in scenarios where you want to run your callbacks in parallel with the rest of your code.
- Clean-up tasks: By using the "on_end" callback, you can specify what to do after a function has finished executing, for example to release resources or close connections.
- Asynchronous communication between microservices in a microservice architecture.
- Improving the performance of long-running processes by breaking them into smaller, asynchronous tasks.
- Creating real-time, event-driven architectures for web applications, gaming, or IoT applications.
- Implementing the Observer pattern for decoupled event-driven communication between different parts of an application.

### Instalation
Package is currently available under the same name at [![PyPI version](https://badge.fury.io/py/callpyback.svg)](https://badge.fury.io/py/callpyback).

`pip install callpyback`

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Usage

### ! important note !
In latest version of `callpyback`, when declaring callback functions, following rules must be obeyed:

a) `on_call()` callback MUST eitheraccept no parameters or combination of the following:
- `func` - will receive reference to decorated function
- `func_kwargs` - will receive parameters passed to the function decorated with `CallPyBack`

b) `on_success()` callback MUST either accept no parameters or combination of the following:
- `func` - will receive reference to decorated function
- `func_result` - will receive return value of the function decorated with `CallPyBack`
- `func_kwargs` - will receive parameters passed to the function decorated with `CallPyBack`

c) `on_failure()` callback MUST either accept no parameters or combination of the following:
- `func` - will receive reference to decorated function
- `func_exception` - will receive exception raised by the function decorated with `CallPyBack`
- `func_kwargs` - will receive parameters passed to the function decorated with `CallPyBack`

d) `on_end()` callback MUST either accept no parameters or combination of the following:
- `func` - will receive reference to decorated function
- `func_result` - will receive return value of the function decorated with `CallPyBack`
- `func_exception` - will receive exception raised by the function decorated with `CallPyBack`
- `func_kwargs` - will receive parameters passed to the function decorated with `CallPyBack`
- `func_scope_vars` - will receive local variables of the function decorated with `CallPyBack`, whose names were specified in the `pass_vars` decorator parameter.

These rules are enforced to allow omitting parameters in the callback function. This is useful when some of these parameters are not needed for the callback function. If those rules are not obeyed, error will be raised during the initialization of the `CallPyBack` decorator class.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Prerequisites
Consider following callbacks:
```python
def on_call(func, func_kwargs):
    print('-----ON CALL CALLBACK-----')
    func_kwargs_repr = ', '.join(f'{key}={val}' for key, val in func_kwargs.items())
    print(f'Function `{func.__name__}` called with parameters: {func_kwargs_repr}.\n')

@background_callpyback
def on_success(func, func_result, func_kwargs):
    print('-----ON SUCCESS CALLBACK-----')
    func_kwargs_repr = ', '.join(f'{key}={val}' for key, val in func_kwargs.items())
    print(f'Function `{func.__name__}` successfully done with a result: {func_result}.')
    print(f'Was called with parameters: {func_kwargs_repr}\n')

@background_callpyback
def on_failure(func, func_exception, func_kwargs):
    print('-----ON FAILURE CALLBACK-----')
    func_kwargs_repr = ', '.join(f'{key}={val}' for key, val in func_kwargs.items())
    print(f'Function `{func.__name__} failed with an error: {func_exception}!')
    print(f'Was called with parameters: {func_kwargs_repr}\n')

@background_callpyback
def on_end(func, func_result, func_exception, func_kwargs, func_scope_vars):
    print('-----ON END CALLBACK-----')
    func_kwargs_repr = ', '.join(f'{key}={val}' for key, val in func_kwargs.items())
    func_scope_vars_repr = ', '.join(f'{key}={val}' for key, val in func_scope_vars.items())
    if func_exception:
        print(f'Function `{func.__name__} failed with an error: {func_exception}!')
    else:
        print('No exception was raised')
    print(f'Function `{func.__name__}` done with a result: {func_result}.')
    print(f'Was called with parameters: {func_kwargs_repr}')
    print(f'Local variables of the function: {func_scope_vars_repr}')
```
and initialization of a decorator:
```python
custom_callpyback = CallPyBack(
    on_call=on_call,
    on_success=on_success,
    on_failure=on_failure,
    on_end=on_end,
    default_return='default', 
    exception_classes=(RuntimeError,),
    pass_vars=('a',)
)
```
These will be used in following examples:

#### 1. Decorated function executes without error
```python

@custom_callpyback
def method(x, y, z=None):
    a = 42
    return x + y

result = method(1, 2)
print(f'Result: {result}')
```
will result in
```bash
-----ON CALL CALLBACK-----
Function `method` called with parameters: x=1, y=2, z=None.

Result: 3

-----ON SUCCESS CALLBACK-----
Function `method` successfully done with a result: 3.
Was called with parameters: x=1, y=2, z=None

-----ON END CALLBACK-----
No exception was raised
Function `method` done with a result: 3.
Was called with parameters: x=1, y=2, z=None
Local variables of the function: a=42

```
`on_success` and `on_end` will be executed on the background thread, while `on_call` will be executed in a blocking way and `on_failure` will not be called.

#### 2. Decorated function raises an error
```python

@custom_callpyback
def method(x, y, z=None):
    a = 42
    raise RuntimeError("some error")

result = method(1, 2)
print(f'Result: {result}')
```
will result in
```bash
-----ON CALL CALLBACK-----
Function `method` called with parameters: x=1, y=2, z=None.

-----ON FAILURE CALLBACK-----
Function `method` failed with an error: some error!
Was called with parameters: x=1, y=2, z=None

-----ON END CALLBACK-----
Function `method` failed with an error: some error!
Function `method` done with a result: default.
Was called with parameters: x=1, y=2, z=None
Local variables of the function: a=42

```
`on_failure` and `on_end` will be executed on the background thread, while `on_call` will be executed in a blocking way and `on_success` will not be called.

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
- [x] Option to pass decorated function reference to all callbacks
- [ ] To be determined...

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
