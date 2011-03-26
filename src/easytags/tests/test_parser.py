# -*- coding: utf-8 -*-

'''
Created on 20/02/2011

@author: vbmendes
'''

from django import template
from django.test import TestCase

from easytags.node import EasyNode, EasyAsNode


class ParserTests(TestCase):

    def test_environment(self):
        """
            Just make sure everything is set up correctly.
        """
        self.assertTrue(True)

    def test_parse_tag_with_args(self):
        """
            Tests if the parser recognizes one tag and parses its args
        """
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name "arg1" "arg2"')
        self.assertEquals(
            {'args': ('"arg1"', '"arg2"'), 'kwargs': {}},
            EasyNode.parse_to_args_kwargs(parser, token)
        )
    
    def test_parse_tag_with_kwargs(self):
        """
            Tests if the parser recognizes one tag and parses its kwargs
        """
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name kwarg1="1" kwarg2="2"')
        self.assertEquals(
            {'args': (), 'kwargs': {'kwarg1': '"1"', 'kwarg2': '"2"'}},
            EasyNode.parse_to_args_kwargs(parser, token)
        )
    
    def test_parse_tag_with_args_and_kwargs(self):
        """
            Tests if the parser recognizes one tag and parses its args and kwargs
        """
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name "arg1" kwarg1="1"')
        self.assertEquals(
            {'args': ('"arg1"',), 'kwargs': {'kwarg1': '"1"'}},
            EasyNode.parse_to_args_kwargs(parser, token)
        )

    def test_parse_tag_with_variable_arg(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name argvariable')
        self.assertEquals(
            {'args': ('argvariable',), 'kwargs': {}},
            EasyNode.parse_to_args_kwargs(parser, token)
        )
    
    def test_parse_tag_with_equals_in_arg_value(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name "a=1"')
        self.assertEquals(
            {'args': ('"a=1"',), 'kwargs': {}},
            EasyNode.parse_to_args_kwargs(parser, token)
        )
    
    def test_parse_tag_with_equals_in_kwarg_value(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name kwarg1="a=1"')
        self.assertEquals(
            {'args': (), 'kwargs': {'kwarg1': '"a=1"'}},
            EasyNode.parse_to_args_kwargs(parser, token)
        )

    def test_parse_tag_special_symbol_in_arg_value(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, u'tag_name "será?"')
        self.assertEquals(
            {'args': (u'"será?"',), 'kwargs': {}},
            EasyNode.parse_to_args_kwargs(parser, token)
        )

    def test_parse_tag_special_symbol_in_kwarg_value(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, u'tag_name kwarg1="será?"')
        self.assertEquals(
            {'args': (), 'kwargs': {'kwarg1': u'"será?"'}},
            EasyNode.parse_to_args_kwargs(parser, token)
        )

    def test_parse_tag_with_args_after_kwargs_raises_exception(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, u'tag_name kwarg1="será?" my_arg')
        self.assertRaises(template.TemplateSyntaxError,
            EasyNode.parse_to_args_kwargs, parser, token
        )
    
    def test_parse_as_tag_with_args(self):
        """
            Tests if the parser recognizes one tag and parses its args even when using EasyAsNode
        """
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name "arg1" "arg2"')
        self.assertEquals(
            {'args': ('"arg1"', '"arg2"'), 'kwargs': {}, 'varname': None},
            EasyAsNode.parse_to_args_kwargs(parser, token)
        )

    def test_parse_as_tag_with_args_and_as_parameter(self):
        """
            Tests if the parser recognizes one tag and parses its args and as parameter
        """
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name "arg1" "arg2" as varname')
        self.assertEquals(
            {'args': ('"arg1"', '"arg2"'), 'kwargs': {}, 'varname': 'varname'},
            EasyAsNode.parse_to_args_kwargs(parser, token)
        )
