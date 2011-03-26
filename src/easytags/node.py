# -*- coding: utf-8 -*-

'''
Created on 20/02/2011

@author: vbmendes
'''

from inspect import getargspec

from django.template import Node, Variable, TemplateSyntaxError


is_kwarg = lambda bit: not bit[0] in (u'"', u"'") and u'=' in bit


def get_args_kwargs_from_bits(bits):
    args = []
    kwargs = {}
    for bit in bits:
        if is_kwarg(bit):
            splitted_bit = bit.split(u'=')
            kwargs[splitted_bit[0]] = u'='.join(splitted_bit[1:])
        else:
            if not kwargs:
                args.append(bit)
            else:
                raise TemplateSyntaxError(u"Args must be before kwargs.")
                
    return {'args': tuple(args), 'kwargs': kwargs}


class EasyNode(Node):
    
    @classmethod
    def parse_to_args_kwargs(cls, parser, token):
        bits = token.split_contents()
        return get_args_kwargs_from_bits(bits[1:])
    
    @classmethod
    def parse(cls, parser, token):
        args_kwargs = cls.parse_to_args_kwargs(parser, token)
        cls.is_args_kwargs_valid(args_kwargs)
        return cls(args_kwargs)
    
    @classmethod
    def get_argspec(cls, func = None):
        func = func or cls.render_context
        return getargspec(func)
    
    @classmethod
    def is_args_kwargs_valid(cls, args_kwargs):
        render_context_spec = cls.get_argspec()
        
        args = args_kwargs['args']
        kwargs = args_kwargs['kwargs']
        
        valid_args_names = render_context_spec.args
        if 'self' in valid_args_names: valid_args_names.remove('self')
        if 'context' in valid_args_names: valid_args_names.remove('context')
        
        n_args_kwargs = len(args) + len(kwargs)
        
        max_n_args_kwargs = len(valid_args_names) 
        if not render_context_spec.varargs and not render_context_spec.keywords and n_args_kwargs > max_n_args_kwargs:
            raise TemplateSyntaxError(u'Invalid number of args %s (max. %s)' % (n_args_kwargs, max_n_args_kwargs))
        
        min_n_args_kwargs = max_n_args_kwargs - len(render_context_spec.defaults or ())
        if n_args_kwargs < min_n_args_kwargs:
            raise TemplateSyntaxError(u'Invalid number of args %s (min. %s)' % (n_args_kwargs, max_n_args_kwargs))
        
        required_args_names = valid_args_names[len(args):min_n_args_kwargs]
        for required_arg_name in required_args_names:
            if not required_arg_name in kwargs:
                raise TemplateSyntaxError(u'Required arg missing: %s' % required_arg_name)
        
        first_kwarg_index = len(args)
        if not render_context_spec.keywords:
            valid_kwargs = valid_args_names[first_kwarg_index:]
            for kwarg in kwargs:
                if not kwarg in valid_kwargs:
                    raise TemplateSyntaxError(u'Invalid kwarg %s.' % kwarg)
        else:
            defined_args = valid_args_names[:first_kwarg_index]
            for kwarg in kwargs:
                if kwarg in defined_args:
                    raise TemplateSyntaxError(u'%s was defined twice.' % kwarg) 
    
    def __init__(self, args_kwargs):
        self.args = [Variable(arg) for arg in args_kwargs['args']]
        self.kwargs = dict((key, Variable(value)) for key, value in args_kwargs['kwargs'].items())
    
    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict((key, value.resolve(context)) for key, value in self.kwargs.items())
        return self.render_context(context, *args, **kwargs)
    
    def render_context(self, context, *args, **kwargs):
        raise NotImplementedError


class EasyAsNode(EasyNode):
    
    @classmethod
    def parse_to_args_kwargs(cls, parser, token):
        bits = token.split_contents()[1:]
        if len(bits) >= 2 and bits[-2] == 'as':
            varname = bits[-1]
            bits = bits[:-2]
        else:
            varname = None
        args_kwargs = get_args_kwargs_from_bits(bits)
        args_kwargs['varname'] = varname
        return args_kwargs
    
    def __init__(self, args_kwargs):
        super(EasyAsNode, self).__init__(args_kwargs)
        self.varname = args_kwargs['varname']
    
    def render(self, context):
        rendered = super(EasyAsNode, self).render(context)
        if self.varname:
            context[self.varname] = rendered
            return u''
        return rendered
