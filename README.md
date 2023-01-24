# pyback

### Features

- create callbacks for any functions
	- on_success()
	- on_fail(ex)
	- on_end()
- 3 ways to use:
	- `pyback()` decorator function
	- `PyBack` decorator class
	- predefined instance of `PyBack` class for more readable code

###Instalation
`pip install pyback`

###Usage

####```pyback``` callback decorator

##### example callback methods
```python
def func_on_success():
    print("success!")

def func_on_fail(ex):
    print(f"Failed with exception {ex}")

def func_on_end():
    print("ending...")
```
##### case #1 - normal execution without exception
```python
@pyback(on_success=func_on_success, on_fail=func_on_fail, on_end=func_on_end)
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
##### case #2 - execution with exception
```python
@pyback(on_success=func_on_success, on_fail=func_on_fail, on_end=func_on_end)
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
####```PyBack``` callback class
```python
@PyBack(on_success=func_on_success, on_fail=func_on_fail, on_end=func_on_end)
def method()
	pass

method()
```
Will produce the same results as `pyback` decorator. Can be extended further.

####Preconfigured ```PyBack``` callback custom class
```python
custom_pyback = PyBack(
    on_success=func_on_success, on_fail=func_on_fail, on_end=func_on_end
)

@custom_pyback
def method():
	pass

method()
```
Will produce the same results as `pyback` decorator and `PyBack` class. Can be preconfigured to use specific callback functions with initiating a `PyBack` class instance.