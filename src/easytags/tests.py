
from django import template
from django.test import TestCase

from easytags.parser import get_args_kwargs_from_token_parse

class EasyTagsTests(TestCase):

    def test_environment(self):
        """
            Just make sure everything is set up correctly.
        """
        self.assertTrue(True)

    def test_parse_tag_with_args(self):
        """
            Tests if the parser recognizes one tag.
        """
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name arg1 arg2')
        self.assertEquals(
            {'args': ('arg1', 'arg2'), 'kwargs': {}},
            get_args_kwargs_from_token_parse(parser, token)
        )
    
    def test_parse_kwargs_tag(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name arg1="1" arg2="2"')
        self.assertEquals(
            {'args': (), 'kwargs': {'arg1': '"1"', 'arg2': '"2"'}},
            get_args_kwargs_from_token_parse(parser, token)
        )
