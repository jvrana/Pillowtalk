from pillowtalk.exceptions import PillowtalkInitializerError


def validate_init(fxn):
    """ Raises errors for dynamically generated __init__ definitions """

    def wrapped(*args, **kwargs):
        self = args[0]
        args = args[1:]
        fields = self.__class__.FIELDS
        field_dict = {}
        if len(args) > len(fields):
            raise TypeError("Expected {0} arguments but got {1} for {2}.__init__".format(
                    len(fields), len(args), self.__class__.__name__))
        for key, val in kwargs.items():
            if key in field_dict:
                raise PillowtalkInitializerError("{0} got multiple values for {1}".format(self.__class__.__name__, key))
            else:
                field_dict[key] = val
        for field in fields:
            if field not in field_dict.keys():
                raise PillowtalkInitializerError("{0} is missing argument {1}".format(self.__class__.__name__, field))
        return fxn(self, (), **field_dict)

    return wrapped