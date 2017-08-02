# tkvariables
Enhanced tk Variables that add some common sense. Dropin replacement for tk variables for most use cases. This will break your code if you use the arguments provided by the trace callback or if you use the trace ID returned from `trace`. 

```python
import tkvariables as tkv
#...
tkv.IntVar(self, value=42)
```

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
 
Also works with other tk.Variables (including tkv.Variables) as a shortcut to `variable.set(variable.get() + other_variable.get())`. 

## Limits

You can specify a limit with the `min` and `max` arguments. Obviously this will lead to odd results if used with a StringVar.

```python
variable = tkv.IntVar(min=0, max=10)
```

These can be updated after initialization like any other attribute:

```python
variable.max = 20
```

## Trace will accept a list of functions

```python
variable.trace('w', [logger, gui_update, sanity_check])
```

## Set trace functions in the initialization

Added `trace_w` etc argument to the initialization. 

```python
variable = tkv.IntVar(trace_o = [gui_update, sanity_check], trace_w=logger)
```

## todo
* implement deleteing traced functions by disableing `trace_vdelete` and adding a 'delete' option. 
