#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

try:
	import Tkinter as tk
except ImportError:
	import tkinter as tk

class _Base:
	def __init__(self):
		self.old_value = self.get()
		self.get_funcs = []
		self.set_funcs = []
		self.onchange_funcs = []

	def trace(self, mode, func):
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

	def __iadd__(self, value):
		self.set(self.get() + value)
		return self

	def __isub__(self, value):
		self.set(self.get() - value)
		return self

	def __imul__(self, value):
		self.set(self.get() * value)
		return self

	def __imul__(self, value):
		self.set(self.get() * value)
		return self

	def __idiv__(self, value):
		self.set(self.get() / value)
		return self

	def __ifloordiv__(self, value):
		self.set(self.get() // value)
		return self

class StringVar(_Base, tk.StringVar):
	def __init__(self, *args, **kwargs):
		tk.StringVar.__init__(self, *args, **kwargs)
		tk.StringVar.trace(self, 'w', self.run_set)
		_Base.__init__(self)
		tk.StringVar.trace(self, 'r', self.run_get)

class IntVar(_Base, tk.IntVar):
	def __init__(self, *args, **kwargs):
		tk.IntVar.__init__(self, *args, **kwargs)
		tk.IntVar.trace(self, 'w', self.run_set)
		_Base.__init__(self)
		tk.IntVar.trace(self, 'r', self.run_get)

class DoubleVar(_Base, tk.DoubleVar):
	def __init__(self, *args, **kwargs):
		tk.DoubleVar.__init__(self, *args, **kwargs)
		tk.DoubleVar.trace(self, 'w', self.run_set)
		_Base.__init__(self)
		tk.DoubleVar.trace(self, 'r', self.run_get)

class BooleanVar(_Base, tk.BooleanVar):
	def __init__(self, *args, **kwargs):
		tk.BooleanVar.__init__(self, *args, **kwargs)
		tk.BooleanVar.trace(self, 'w', self.run_set)
		_Base.__init__(self)
		tk.BooleanVar.trace(self, 'r', self.run_get)

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
	options = 'spam and eggs'.split()
	var = StringVar(value=options[0])
	var.trace('w', set_callback)
	var.trace('o', onchange_callback)
	var.trace('r', get_callback)
	ent = tk.OptionMenu(r, var, *options)
	ent.pack()

	f = tk.Frame(r)
	counter = IntVar()
	btn = tk.Button(f, text='-', command=decrement)
	btn.pack(side=tk.LEFT)
	lbl = tk.Label(f, textvariable=counter)
	lbl.pack(side=tk.LEFT)
	btn = tk.Button(f, text='+', command=increment)
	btn.pack(side=tk.LEFT)
	f.pack()

	r.mainloop()

if __name__ == "__main__":
	main()
