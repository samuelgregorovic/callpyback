# callpyback

### Features

- on_call callback
- on_success callback
- on_failure callback
- on_end callback
- default return
- using local variables of function in on_end
- support for async/sync callbacks with auto-detect
- support for omitting callback functions parameters with auto-detect
- pre-defining custom callback with creating class instance and using it as decorator


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
