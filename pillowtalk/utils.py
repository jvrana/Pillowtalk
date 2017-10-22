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
        for i, a in enumerate(args):
            f = fields[i]
            field_dict[f] = a
        for k, v in kwargs.items():
            if k in field_dict:
                raise PillowtalkInitializerError("Got multiple values for {0}".format(k))
            else:
                field_dict[k] = v
        for f in fields:
            if f not in field_dict.keys():
                raise PillowtalkInitializerError("Missing argument for {0}".format(f))
        return fxn(self, (), **field_dict)

    return wrapped