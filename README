django-meio-easytags
====================

An easy way to create custom template tags for Django's templating system.

Usage
=====

Just instantiate EasyLibrary and register the renderer method as a template tag::

	from easytags import EasyLibrary
	
	register = EasyLibrary()
	
    def sum(context, arg1, arg2, arg3=0):
        return int(arg1) + int(arg2) + int(arg3)
	
	register.easytag(sum)

The EasyLibrary will take care of subclassing EasyNode that will take care of 
the template tag's parsing, resolving variable and inspecting if the args are 
ok with the renderer signature. In the example above, you can use
the sum tag in any of the forms below::

	{% sum "1" "2" %}
	{% sum "1" arg2="2" %}
	{% sum arg1="1" arg2="2" %}
	{% sum arg2="2" arg1="1" %}

It's almost like calling methods in Python.

In this example, ``arg3`` is optional and defaults to 0. So you may use or not this arg.

