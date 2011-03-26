# -*- coding: utf-8 -*-

'''
Created on 01/03/2011

@author: vbmendes
'''

import unittest

from django import template

from easytags import EasyLibrary
from easytags import EasyNode, EasyAsNode

class LibraryTests(unittest.TestCase):

    def test_easy_library_register_easy_node(self):
        def test_tag(context):
            return u'my return'

        register = EasyLibrary()
        register.easytag(test_tag)
        
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'test_tag')
        
        self.assertTrue(register.tags.has_key('test_tag'))
        
        test_node = register.tags['test_tag'](parser, token)
        
        self.assertTrue(isinstance(test_node, EasyNode))
        
        context = template.Context({})
        
        self.assertEquals(u'my return', test_node.render(context))
    
    def test_easy_library_register_easy_node_with_parameters(self):
        def test_tag(context, arg1):
            return arg1

        register = EasyLibrary()
        register.easytag(test_tag)
        
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'test_tag "my arg"')
        test_node = register.tags['test_tag'](parser, token)
        
        context = template.Context({})
        self.assertEquals(u'my arg', test_node.render(context))
    
    def test_easy_library_register_tags_with_custom_names(self):
        def test_tag(context):
            return u''

        register = EasyLibrary()
        register.easytag('tag_name', test_tag)

        self.assertTrue(register.tags.has_key('tag_name'))
    
    def test_easy_library_register_tags_as_decorating_method(self):
        def test_tag(context):
            return u''

        register = EasyLibrary()
        register.easytag()(test_tag)

        self.assertTrue(register.tags.has_key('test_tag'))
    
    def test_easy_library_register_tags_as_decorating_method_with_name(self):
        def test_tag(context):
            return u''

        register = EasyLibrary()
        register.easytag('tag_name')(test_tag)

        self.assertTrue(register.tags.has_key('tag_name'))
    
    def test_easy_library_register_tags_as_decorating_method_with_name_kwarg(self):
        def test_tag(context):
            return u''

        register = EasyLibrary()
        register.easytag(name='tag_name')(test_tag)

        self.assertTrue(register.tags.has_key('tag_name'))
    
    def test_easy_library_register_tags_keeps_decorated_function_data(self):
        def test_tag(context):
            return u''

        register = EasyLibrary()
        test_tag = register.easytag(name='tag_name')(test_tag)

        self.assertEquals('test_tag', test_tag.__name__)
    
        
    def test_easy_library_register_as_tags(self):
        def test_tag(context):
            return u'my return'

        register = EasyLibrary()
        register.easyastag(test_tag)
        
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'test_tag as varname')
        
        self.assertTrue(register.tags.has_key('test_tag'))
        
        test_node = register.tags['test_tag'](parser, token)
        
        self.assertTrue(isinstance(test_node, EasyAsNode))
        
        context = template.Context({})
        
        self.assertEquals(u'', test_node.render(context))
        self.assertEquals(u'my return', context['varname'])
