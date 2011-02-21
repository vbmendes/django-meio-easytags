# -*- coding: utf-8 -*-

'''
Created on 20/02/2011

@author: vbmendes
'''

from django.template import Context, Variable
from django.test import TestCase

from easytags.node import EasyNode

class MyEasyNode(EasyNode):

    def render_context(self, arg1):
        return arg1

class NodeTests(TestCase):
    
    def test_resolves_absolute_string(self):
        context = Context({})
        args_kwargs = {'args': ('"absolute string"',), 'kwargs': {}}
        
        node = MyEasyNode(args_kwargs)
    
        self.assertEquals(
            u'absolute string',
            node.render(context),
        )

    def test_resolve_simple_variable(self):
        context = Context({'simple_variable': u'simple variable value'})
        args_kwargs = {'args': ('simple_variable',), 'kwargs': {}}
        
        node = MyEasyNode(args_kwargs)
    
        self.assertEquals(
            u'simple variable value',
            node.render(context),
        )
    
    def test_resolve_dict_variable(self):
        context = Context({'mydict': {'key': u'value'}})
        args_kwargs = {'args': ('mydict.key',), 'kwargs': {}}
        
        node = MyEasyNode(args_kwargs)
    
        self.assertEquals(
            u'value',
            node.render(context),
        )
    
    def test_resolve_absolute_string_in_kwargs(self):
        context = Context({})
        args_kwargs = {'args': (), 'kwargs': {'arg1': u'"absolute string"'}}
        
        node = MyEasyNode(args_kwargs)
        
        self.assertEquals(
            u'absolute string',
            node.render(context),
        )
    
    def test_resolve_simple_variable_in_kwargs(self):
        context = Context({'simple_variable': u'simple variable value'})
        args_kwargs = {'args': (), 'kwargs': {'arg1': u'simple_variable'}}
        
        node = MyEasyNode(args_kwargs)
        
        self.assertEquals(
            u'simple variable value',
            node.render(context),
        )
    
    def test_resolve_dict_variable_in_kwargs(self):
        context = Context({'mydict': {'key': u'value'}})
        args_kwargs = {'args': (), 'kwargs': {'arg1': 'mydict.key'}}
        
        node = MyEasyNode(args_kwargs)
        
        self.assertEquals(
            u'value',
            node.render(context),
        )
