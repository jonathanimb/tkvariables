# tkvariables
Enhanced tk Variables that add some common sense. 

## Useful arguments on trace functions

Using `variable.trace` adds callback functions. These callbacks are usually called with useless arguments. Here the functions are called with 3 arguments: the new value, the old value, and the variable itself: 

```python
def callback(new, old, var):
    print("the {} variable was changed from {} to {}.".format(var, old, new))
```

## Trigger the callback only when the variable changes. 

When a user selects a dropdown just to see the options, but does not change anything, there is no reason to trigger your callback. The new 'o' mode only triggers when the value of the variable changes. 

```python
variable.trace('o', callback)
```

## Add inplace math

Added common inplace math. 

```python
variable += 1
```
 As a shortcut to the very cumbersome `variable.set(variable.get() + 1)`. 
