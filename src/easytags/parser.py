# -*- coding: utf-8 -*-

'''
Created on 20/02/2011

@author: vbmendes
'''

from django.template import TemplateSyntaxError


def get_args_kwargs_from_token_parse(parser, token):
    bits = token.split_contents()
    args = []
    kwargs = {}

    for bit in bits[1:]:
        splitted_bit = bit.split(u'=')
        if not bit[0] in (u'"', u"'") and len(splitted_bit) > 1:
            kwargs[splitted_bit[0]] = u'='.join(splitted_bit[1:])
        elif not kwargs:
            args.append(u'='.join(splitted_bit))
        else:
            raise TemplateSyntaxError(u"Args must be before kwargs.")
            
    return {'args': tuple(args), 'kwargs': kwargs}
