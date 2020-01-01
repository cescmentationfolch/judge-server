import os
import re

from dmoj.utils.load import get_available_modules, load_module, load_modules

_recontribmodule = re.compile(r'([a-z]+)\.py')

contrib_modules = {}

def get_available():
    return get_available_modules(_recontribmodule, os.path.dirname(__file__), None, None)


def load_contrib_module(name):
    return load_module('%s.%s' % (__name__, name), ())

def load_contrib_modules():
    load_modules(get_available(), load_executor, 'ContribModule', contrib_modules, (),
                 'Loading third party modules...')