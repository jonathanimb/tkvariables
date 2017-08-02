#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

try:
	import Tkinter as tk
except ImportError:
	import tkinter as tk

class _Base:
	def __init__(self, master=None, min=None, max=None, trace_w=None, trace_o=None, trace_r=None, **kwargs):
		self.min = min
		self.max = max
		self.get_funcs = []
		self.set_funcs = []
		self.onchange_funcs = []

		self.tk_super.__init__(self, master, **kwargs)
		self.tk_super.trace(self, 'w', self.run_set)
		self.old_value = self.get()
		self.tk_super.trace(self, 'r', self.run_get)

		self.trace('w', trace_w)
		self.trace('o', trace_o)
		self.trace('r', trace_r)

	def set(self, value):
		if self.min is not None and value < self.min:
			value = self.min
		if self.max is not None and value > self.max:
			value = self.max
		self.tk_super.set(self, value)

	def trace(self, mode, funcs, delete=False):
		if funcs is None:
			return
		if not isinstance(funcs, (list, tuple)):
			funcs = [funcs]
		for func in funcs:
			if mode == 'w':
				self.set_funcs.append(func)
			elif mode == 'r':
				self.get_funcs.append(func)
			elif mode == 'o':
				self.onchange_funcs.append(func)
			else:
				raise ValueError('mode {!r} is not known'.format(mode))

	def run_get(self, *useless_args):
		for func in self.get_funcs:
			func(self.get(), self.get(), self)

	def run_set(self, *useless_args):
		new_value = self.get()
		for func in self.set_funcs:
			func(new_value, self.old_value, self)
		if self.old_value != new_value:
			for func in self.onchange_funcs:
				func(new_value, self.old_value, self)
		self.old_value = new_value

	def _get_value(self, other):
		if isinstance(other, tk.Variable):
			return other.get()
		else:
			return other

	def __iadd__(self, other):
		self.set(self.get() + self._get_value(other))
		return self

	def __isub__(self, other):
		self.set(self.get() - self._get_value(other))
		return self

	def __imul__(self, other):
		self.set(self.get() * self._get_value(other))
		return self

	def __imul__(self, other):
		self.set(self.get() * self._get_value(other))
		return self

	def __idiv__(self, other):
		self.set(self.get() / self._get_value(other))
		return self

	def __ifloordiv__(self, other):
		self.set(self.get() // self._get_value(other))
		return self

class StringVar(_Base, tk.StringVar):
	def __init__(self, *args, **kwargs):
		self.tk_super = tk.StringVar
		_Base.__init__(self, *args, **kwargs)

class IntVar(_Base, tk.IntVar):
	def __init__(self, *args, **kwargs):
		self.tk_super = tk.IntVar
		_Base.__init__(self, *args, **kwargs)

class DoubleVar(_Base, tk.DoubleVar):
	def __init__(self, *args, **kwargs):
		self.tk_super = tk.DoubleVar
		_Base.__init__(self, *args, **kwargs)

class BooleanVar(_Base, tk.BooleanVar):
	def __init__(self, *args, **kwargs):
		self.tk_super = tk.BooleanVar
		_Base.__init__(self, *args, **kwargs)


##debug / demo
def set_callback(new, old, var):
	print("the {} variable was set. (was {!r} now {!r}).".format(var, old, new))

def get_callback(new, old, var):
	print("the {} variable was got. (was {!r} now {!r}).".format(var, old, new))

def onchange_callback(new, old, var):
	print("the {} variable was changed. (was {!r} now {!r}).".format(var, old, new))

def increment():
	global counter
	counter += 1
def decrement():
	global counter
	counter -= 1

def main():
	global counter
	r = tk.Tk()
	r.geometry('300x300')

	options = 'spam and eggs'.split()
	var = StringVar(value=options[0])
	var.trace('w', set_callback)
	var.trace('o', onchange_callback)
	var.trace('r', get_callback)
	ent = tk.OptionMenu(r, var, *options)
	ent.pack()

	f = tk.Frame(r)
	counter = IntVar(min=-2, max=15)
	btn = tk.Button(f, text='-', command=decrement)
	btn.pack(side=tk.LEFT)
	lbl = tk.Label(f, textvariable=counter)
	lbl.pack(side=tk.LEFT)
	btn = tk.Button(f, text='+', command=increment)
	btn.pack(side=tk.LEFT)
	other = IntVar(value=10)
	def add10():
		global counter
		counter += other
	btn = tk.Button(f, text='+10', command=add10)
	btn.pack(side=tk.LEFT)
	f.pack()

	r.mainloop()

if __name__ == "__main__":
	main()

