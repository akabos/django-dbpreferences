# coding: utf-8
from django.db.models.loading import AppCache
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule

from dbpreferences.conf import PREF_FORM_FILENAME


__all__ = ('get_app_preferences',)


class DBPpeferencesAppCache(AppCache):

    def load_app(self, app_name, can_postpone=False):
        """
        Returns app's preferences module

        Had to copy it from parent class (as in Django 1.2.4), because
        there's no way to customize module name this utility belives to be 'app'
        """
        self.handled[app_name] = None
        self.nesting_level += 1
        app_module = import_module(app_name)
        try:
            prefs = import_module('.%s' % PREF_FORM_FILENAME, app_name)
        except ImportError:
            self.nesting_level -= 1
            if not module_has_submodule(app_module, PREF_FORM_FILENAME):
                return None
            else:
                if can_postpone:
                    self.postponed.append(app_name)
                    return None
                else:
                    raise

        self.nesting_level -= 1
        if prefs not in self.app_store:
            self.app_store[prefs] = len(self.app_store)
        return prefs


cache = DBPpeferencesAppCache()

get_app = cache.get_app
