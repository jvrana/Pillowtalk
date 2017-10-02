import re
from marshmallow import pprint

class Utils(object):
    """ Utilities """

    @staticmethod
    def snake_to_camel(s):
        return s.replace("_", " ").title().replace(" ", "")

    @staticmethod
    def camel_to_snake(s):
        return "_".join(re.findall('[A-Z][^A-Z]*', s)).lower()

utils = Utils
