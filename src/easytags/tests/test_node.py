# -*- coding: utf-8 -*-

'''
Created on 20/02/2011

@author: vbmendes
'''

from django import template
from django.template import Context, Variable, TemplateSyntaxError
from django.test import TestCase

from easytags.node import EasyNode, EasyAsNode


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

        self.assertRaises(TemplateSyntaxError, MyEasyNode.parse, parser, token)
    
    def test_node_parse_verifies_kwarg_already_satisfied_by_arg(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name arg1 arg1="a=1"')

        self.assertRaises(TemplateSyntaxError, MyEasyNode.parse, parser, token)
    
    def test_node_parse_verifies_if_there_are_more_args_kwargs_then_method_requires(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name arg1 arg2 arg3')

        self.assertRaises(TemplateSyntaxError, MyEasyNode.parse, parser, token)

    def test_node_parse_verifies_if_there_are_less_args_kwargs_then_method_requires(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name')

        self.assertRaises(TemplateSyntaxError, MyEasyNode.parse, parser, token)

    def test_node_parse_verifies_if_required_arg_is_specified(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name kwarg1="a"')

        self.assertRaises(TemplateSyntaxError, MyEasyNode.parse, parser, token)

    def test_node_can_have_no_args_with_default_value(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name "a"')
        
        node = MyEasyNodeWithoutDefaults.parse(parser, token)
        
        self.assertEquals(u'"a"' ,node.args[0].var)
    
    def test_node_can_receive_infinite_args(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name "a" "b" "c" "d"')
        
        MyEasyNode = type('MyEasyNodeWithArgs', (EasyNode,), {
            'render_context': lambda self, context, *args: reduce(lambda x, y: x + y, args)
        })
        
        node = MyEasyNode.parse(parser, token)
        
        self.assertEquals(u'abcd' ,node.render(Context({})))
    
    def test_node_can_receive_required_arg_and_infinite_args(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name "a" "b" "c" "d"')
        
        MyEasyNode = type('MyEasyNode', (EasyNode,), {
            'render_context': lambda self, context, arg1, *args: arg1 + reduce(lambda x, y: x + y, args)
        })
        
        node = MyEasyNode.parse(parser, token) 
        
        self.assertEquals(u'abcd' ,node.render(Context({})))
    
    def test_node_verifies_if_required_arg_is_specified_when_node_can_receive_infinite_args(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name')
        
        MyEasyNode = type('MyEasyNode', (EasyNode,), {
            'render_context': lambda self, context, arg1, *args: True
        })
        
        self.assertRaises(TemplateSyntaxError, MyEasyNode.parse, parser, token)

    def test_node_can_receive_kwargs(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name arg1="bla" arg2="ble"')
        
        MyEasyNode = type('MyEasyNode', (EasyNode,), {
            'render_context': lambda self, context, **kwargs:\
                reduce(lambda x,y: u'%s%s' % (x, y),
                    ['%s=%s' % (key, value) for key, value in kwargs.items()])
        })
        
        node = MyEasyNode.parse(parser, token)
        
        self.assertEquals(u'arg1=blaarg2=ble', node.render(Context({})))

    def test_node_verifies_if_required_arg_is_specified_when_code_can_receive_kwargs(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name')
        
        MyEasyNode = type('MyEasyNode', (EasyNode,), {
            'render_context': lambda self, context, arg1, **kwargs: True
        })
        
        self.assertRaises(TemplateSyntaxError, MyEasyNode.parse, parser, token)

    def test_node_verifies_if_required_kwarg_is_specified_when_code_can_receive_kwargs(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name arg2="2"')
        
        MyEasyNode = type('MyEasyNode', (EasyNode,), {
            'render_context': lambda self, context, arg1, **kwargs: True
        })
        
        self.assertRaises(TemplateSyntaxError, MyEasyNode.parse, parser, token)
    
    def test_if_node_can_receive_args_and_kwargs(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name "1" arg2="2"')
        
        MyEasyNode = type('MyEasyNode', (EasyNode,), {
            'render_context': lambda self, context, *args, **kwargs: 
                args[0]+kwargs.items()[0][0]+u'='+kwargs.items()[0][1]
        })
        
        node = MyEasyNode.parse(parser, token)
        
        self.assertEquals(u'1arg2=2', node.render(Context({})))
    
    def test_if_node_can_receive_required_arg_and_kwargs(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name "required" "2" arg3="3"')
        
        MyEasyNode = type('MyEasyNode', (EasyNode,), {
            'render_context': lambda self, context, arg1, *args, **kwargs: 
                arg1+args[0]+kwargs.items()[0][0]+u'='+kwargs.items()[0][1]
        })
        
        node = MyEasyNode.parse(parser, token)
        
        self.assertEquals(u'required2arg3=3', node.render(Context({})))
    
    def test_node_verifies_if_required_arg_is_specified_two_times(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name "required" arg1="3"')
        
        MyEasyNode = type('MyEasyNode', (EasyNode,), {
            'render_context': lambda self, context, arg1, *args, **kwargs: True
        })
        
        self.assertRaises(TemplateSyntaxError, MyEasyNode.parse, parser, token)
        
    def test_as_node_receives_as_parameter(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, u'tag_name as varname')
        
        MyEasyAsNode = type('MyEasyAsNode', (EasyAsNode,), {
            'render_context': lambda self, context, **kwargs: 'value'
        })
        
        node = MyEasyAsNode.parse(parser, token)
        context = Context()
        
        self.assertEqual('', node.render(context))
        self.assertEqual('value', context['varname']) 
    
    def test_as_node_can_be_used_without_as_parameter(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, u'tag_name "value"')
        
        MyEasyAsNode = type('MyEasyAsNode', (EasyAsNode,), {
            'render_context': lambda self, context, arg1, **kwargs: arg1
        })
        
        node = MyEasyAsNode.parse(parser, token)
        context = Context()
        
        self.assertEqual('value', node.render(context))
        
