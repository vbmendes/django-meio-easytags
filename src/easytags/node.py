# -*- coding: utf-8 -*-

'''
Created on 20/02/2011

@author: vbmendes
'''

from django.template import Node, Variable

class EasyNode(Node):
    
    def __init__(self, args_kwargs):
        self.args = [Variable(arg) for arg in args_kwargs['args']]
        self.kwargs = dict((key, Variable(value)) for key, value in args_kwargs['kwargs'].items())
    
    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict((key, value.resolve(context)) for key, value in self.kwargs.items())
        return self.render_context(*args, **kwargs)
    
    def render_context(self, *args, **kwargs):
        raise NotImplementedError
