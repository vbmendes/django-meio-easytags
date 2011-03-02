# -*- coding: utf-8 -*-

'''
Created on 01/03/2011

@author: vbmendes
'''

from django.template import Library

from node import EasyNode

class EasyLibrary(Library):

    @classmethod
    def _get_name_and_renderer(cls, *args):
        if len(args) == 1:
            renderer = args[0]
            name = renderer.__name__
        else:
            name, renderer = args
        return name, renderer
    
    def easytag(self, *args):
        name, renderer = self.__class__._get_name_and_renderer(*args)
        
        def render_context(self, context, *args, **kwargs):
            return renderer(context, *args, **kwargs)
        
        get_argspec = classmethod(lambda cls: EasyNode.get_argspec(renderer))
        
        tag_node = type('%sEasyNode' % name, (EasyNode,), {
            'render_context': render_context,
            'get_argspec': get_argspec,
        })
        self.tag(name, tag_node.parse)
