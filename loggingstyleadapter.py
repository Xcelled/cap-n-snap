''' This module defines a logging adapter that allows brace-style formatting.

Taken from http://stackoverflow.com/a/24683360/1163742 '''

from inspect import getargspec

NAG = True # Emits statements to fix log strings
if NAG: import traceback, re

class BraceMessage(object):
    def __init__(self, fmt, args, kwargs):
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
    	if NAG and re.search(r'%(\(\w+\))?[#0\-\+ ]?(\.\d+).[diouxXeEfFgGcRsa%]', self.fmt):
    		stack = traceback.extract_tb()
    		print(stack)
    		stack = stack[3]
    		log.debug('FIXME: Old style string interpolation used in {}, {}:{}. Text: "{}"',
    			stack[2], stack[0], stack[1], stack[4])
        return str(self.fmt).format(*self.args, **self.kwargs)

class StyleAdapter(logging.LoggerAdapter):
    def __init__(self, logger):
        self.logger = logger

    def log(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            msg, log_kwargs = self.process(msg, kwargs)
            self.logger._log(level, BraceMessage(msg, args, kwargs), (), 
                    **log_kwargs)

    def process(self, msg, kwargs):
        return msg, {key: kwargs[key] 
                for key in getargspec(self.logger._log).args[1:] if key in kwargs}

import logging
def getLogger(*args, **kwargs): return StyleAdapter(logging.getLogger(*args, **kwargs))

log = getLogger(__name__))
