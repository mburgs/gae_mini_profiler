import os

from google.appengine.api import lib_config

import util

# These should_profile functions return true whenever a request should be
# profiled.
#
# You can override these functions in appengine_config.py. See example below
# and https://developers.google.com/appengine/docs/python/tools/appengineconfig
#
# These functions will be run once per request, so make sure they are fast.
#
# If you need access to the environ use the `with_environ` decorator.
#
# Example:
#   ...in appengine_config.py:
#       def gae_mini_profiler_should_profile_production():
#           from google.appengine.api import users
#           return users.is_current_user_admin()

def _should_profile_production_default():
    """Default to disabling in production if this function isn't overridden.

    Can be overridden in appengine_config.py"""
    return False

def _should_profile_development_default():
    """Default to enabling in development if this function isn't overridden.

    Can be overridden in appengine_config.py"""
    return True

def with_environ(func):
    """Decorator to distinguish should_profile_*() methods that need access
    to the environ"""
    func._accept_environ = True
    return func

_config = lib_config.register("gae_mini_profiler", {
    "should_profile_production": _should_profile_production_default,
    "should_profile_development": _should_profile_development_default})

def should_profile(environ):
    """Returns true if the current request should be profiles."""
    if util.dev_server:
        func = _config.should_profile_development
    else:
        func = _config.should_profile_production

    if getattr(func, '_accept_environ', False):
        args = environ,
    else:
        args = tuple()

    return func(*args)
