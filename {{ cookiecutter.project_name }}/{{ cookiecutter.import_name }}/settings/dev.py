"""
Dev specific settings
"""

from .{{ cookiecutter.import_name }} import *

DEBUG = True

# allow overriding with untracked local.py
try:
    from .local import *
except ImportError:
    pass
