# -*- coding: utf-8 -*-

'''
Created on 20/02/2011

@author: vbmendes
'''

from inspect import getargspec

from django.template import Node, Variable, TemplateSyntaxError

from parser import get_args_kwargs_from_token_parse

class EasyNode(Node):
    
    @classmethod
    def parse(cls, parser, token):
        args_kwargs = get_args_kwargs_from_token_parse(parser, token)
        cls.is_args_kwargs_valid(args_kwargs)
        return cls(args_kwargs)
    
    @classmethod
    def is_args_kwargs_valid(cls, args_kwargs):
        render_context_spec = getargspec(cls.render_context)
        
        args = args_kwargs['args']
        kwargs = args_kwargs['kwargs']
        
        valid_args_names = render_context_spec.args[2:]
        
        n_args_kwargs = len(args) + len(kwargs)
        
        max_n_args_kwargs = len(valid_args_names) 
        if n_args_kwargs > max_n_args_kwargs:
            raise TemplateSyntaxError(u'Invalid number of args %s (max. %s)' % (n_args_kwargs, max_n_args_kwargs))
        
        min_n_args_kwargs = max_n_args_kwargs - len(render_context_spec.defaults)
        if n_args_kwargs < min_n_args_kwargs:
            raise TemplateSyntaxError(u'Invalid number of args %s (min. %s)' % (n_args_kwargs, max_n_args_kwargs))
        
        required_args_names = valid_args_names[len(args):min_n_args_kwargs]
        for required_arg_name in required_args_names:
            if not required_arg_name in kwargs:
                raise TemplateSyntaxError(u'Required arg missing: %s' % required_arg_name)
        
        first_kwarg_index = len(args)
        valid_kwargs = valid_args_names[first_kwarg_index:]
        for kwarg in kwargs:
            if not kwarg in valid_kwargs:
                raise TemplateSyntaxError(u'Invalid kwarg %s.' % kwarg)        
    
    def __init__(self, args_kwargs):
        self.args = [Variable(arg) for arg in args_kwargs['args']]
        self.kwargs = dict((key, Variable(value)) for key, value in args_kwargs['kwargs'].items())
    
    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict((key, value.resolve(context)) for key, value in self.kwargs.items())
        return self.render_context(context, *args, **kwargs)
    
    def render_context(self, context, *args, **kwargs):
        raise NotImplementedError