# callpyback

### Features

- create callbacks for any functions
	- on_success()
	- on_fail(ex)
	- on_end()
- 3 ways to use:
	- `callpyback()` decorator function
	- `CallPyBack` decorator class
	- predefined instance of `CallPyBack` class for more readable code

### Instalation
`pip install callpyback`

### Usage

#### 1. ```callpyback``` callback decorator

##### Callback methods used in example
```python
def func_on_success():
    print("success!")

def func_on_fail(ex):
    print(f"Failed with exception {ex}")

def func_on_end():
    print("ending...")
```
##### Case - normal execution without exception
```python
@callpyback(on_success=func_on_success, on_fail=func_on_fail, on_end=func_on_end)
def method_ok():
    print('method ok')

method_ok()
```
will produce
```python
>>>method ok
>>>success!
>>>ending...
```
##### Case - execution with exception
```python
@callpyback(on_success=func_on_success, on_fail=func_on_fail, on_end=func_on_end)
def method_fail():
    print('method before fail')
	raise Exception('EpicFailure')

method_ok()
```
will produce
```python
>>>method before fail
>>>Failed with exception EpicFailure
>>>ending...
```
#### 2. ```CallPyBack``` callback class
```python
@CallPyBack(on_success=func_on_success, on_fail=func_on_fail, on_end=func_on_end)
def method()
    pass

method()
```
Will produce the same results as `callpyback` decorator. Can be extended further.

#### 3. Preconfigured ```CallPyBack``` callback custom class
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
