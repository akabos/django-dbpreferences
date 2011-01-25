# coding: utf-8
from django.conf import settings

# The filename in witch the form should be stored:
PREF_FORM_FILENAME = getattr(settings, "DBPREFERENCES_FORMS", "preference_forms")
