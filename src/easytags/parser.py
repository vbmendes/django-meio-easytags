# -*- coding: utf-8 -*-

'''
Created on 20/02/2011

@author: vbmendes
'''

from django.template import TemplateSyntaxError


is_kwarg = lambda bit: not bit[0] in (u'"', u"'") and u'=' in bit


def get_args_kwargs_from_token_parse(parser, token):
    bits = token.split_contents()
    args = []
    kwargs = {}
    
    for bit in bits[1:]:
        if is_kwarg(bit):
            splitted_bit = bit.split(u'=')
            kwargs[splitted_bit[0]] = u'='.join(splitted_bit[1:])
        else:
            if not kwargs:
                args.append(bit)
            else:
                raise TemplateSyntaxError(u"Args must be before kwargs.")
                
    return {'args': tuple(args), 'kwargs': kwargs}
