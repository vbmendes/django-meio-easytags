# -*- coding: utf-8 -*-

'''
Created on 01/03/2011

@author: vbmendes
'''

from django.template import Library

from node import EasyNode

class EasyLibrary(Library):

    @classmethod
    def _get_name_and_renderer(cls, name, renderer):
        if not renderer:
            renderer = name
            name = renderer.__name__
        return name, renderer
    
    def easytag(self, name = None, renderer = None):
        if not name and not renderer:
            return self.easytag
        if not renderer:
            if callable(name):
                renderer = name
                return self._register_easytag(renderer.__name__, renderer)
            else:
                def dec(renderer):
                    return self._register_easytag(name, renderer)
                return dec
        return self._register_easytag(name, renderer)
    
    def _register_easytag(self, name, renderer):
        if not renderer:
            renderer = name
            name = renderer.__name__
        
        def render_context(self, context, *args, **kwargs):
            return renderer(context, *args, **kwargs)
        
        get_argspec = classmethod(lambda cls: EasyNode.get_argspec(renderer))
        
        tag_node = type('%sEasyNode' % name, (EasyNode,), {
            'render_context': render_context,
            'get_argspec': get_argspec,
        })
        self.tag(name, tag_node.parse)
        return renderer
