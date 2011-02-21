# -*- coding: utf-8 -*-

'''
Created on 20/02/2011

@author: vbmendes
'''

from django import template
from django.template import Context, Variable
from django.test import TestCase

from easytags.node import EasyNode

class MyEasyNode(EasyNode):

    def render_context(self, context, arg1, kwarg1=None):
        return arg1

class MyEasyNodeWithoutDefaults(EasyNode):

    def render_context(self, context, arg1):
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

    def test_node_parse_returns_node_instance(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name arg1 kwarg1="a=1"')
        node = MyEasyNode.parse(parser, token)
        
        self.assertTrue(isinstance(node, MyEasyNode))
        self.assertEquals(u'arg1', node.args[0].var)
        self.assertEquals(u'"a=1"', node.kwargs['kwarg1'].var)
    
    def test_node_parse_verifies_invalid_kwarg(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name arg1 invalid_kwarg="a=1"')

        self.assertRaises(template.TemplateSyntaxError, MyEasyNode.parse, parser, token)
    
    def test_node_parse_verifies_kwarg_already_satisfied_by_arg(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name arg1 arg1="a=1"')

        self.assertRaises(template.TemplateSyntaxError, MyEasyNode.parse, parser, token)
    
    def test_node_parse_verifies_if_there_are_more_args_kwargs_then_method_requires(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name arg1 arg2 arg3')

        self.assertRaises(template.TemplateSyntaxError, MyEasyNode.parse, parser, token)

    def test_node_parse_verifies_if_there_are_less_args_kwargs_then_method_requires(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name')

        self.assertRaises(template.TemplateSyntaxError, MyEasyNode.parse, parser, token)

    def test_node_parse_verifies_if_required_arg_is_specified(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name kwarg1="a"')

        self.assertRaises(template.TemplateSyntaxError, MyEasyNode.parse, parser, token)

    def test_node_can_have_no_args_with_default_value(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name "a"')
        
        node = MyEasyNodeWithoutDefaults.parse(parser, token)
        
        self.assertEquals(u'"a"' ,node.args[0].var)
