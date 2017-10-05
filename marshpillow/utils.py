import re
from marshmallow import pprint

class Utils(object):
    """ Utilities """

    @staticmethod
    def snake_to_camel(s):
        if Utils.is_snake(s):
            return s.replace("_", " ").title().replace(" ", "")
        else:
            return s

    @staticmethod
    def camel_to_snake(s):
        if Utils.is_camel(s):
            return "_".join(re.findall('[A-Z][^A-Z]*', s)).lower()
        else:
            return s

    @staticmethod
    def is_snake(s):
        return " " not in s and s.lower() == s

    @staticmethod
    def is_camel(s):
        return " " not in s and s[0].isupper()

utils = Utils
