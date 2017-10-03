class Relationship(object):
    def __init__(self, attribute, with_model, with_reference, with_function, with_attribute=None, get_association=None):
        self.attribute = attribute
        self.with_model = with_model
        self.with_reference = with_reference
        self.with_function = with_function
        self.with_attribute = with_attribute
        self.get_association = get_association

    def _get_param_as_attr(self, this):
        pass

    def _get_param_as_dict(self, this):
        pass

    def _get_param(self, this):
        # TODO: When to switch between attr and dict formats?
        if hasattr(this, self.with_reference):
            return getattr(this, self.with_reference)
        elif self.with_reference in this:
            return this[self.with_reference]
        # TODO: or try to interpret "sample_type[id]" to unmarshal dictionary objects

    def fullfill(self, this):
        param = self._get_param(this)
        fxn = self._get_function()
        if self.with_attribute is not None:
            param = {self.with_attribute: param}
        r = fxn(param)
        if self.get_association:
            return [getattr(x, self.get_association) for x in r]
        return r

    def _get_function(self):
        """ Gets the function from the reference model """
        if callable(self.with_function):
            return self.with_function
        elif type(self.with_function) is str:
            return getattr(self.with_model, self.with_function)


class HasOne(Relationship):
    def __init__(self, attribute_name, connect_with_model, use_reference, use_function):
        super().__init__(attribute=attribute_name,
                         with_model=connect_with_model,
                         with_reference=use_reference,
                         with_function=use_function)


class HasMany(Relationship):
    def __init__(self, attribute_name, connect_with_model, use_reference, use_function, model_reference):
        super().__init__(attribute=attribute_name,
                         with_model=connect_with_model,
                         with_reference=use_reference,
                         with_function=use_function,
                         with_attribute=model_reference)


class Association(Relationship):
    def __init__(self, attribute_name, association_model, connect_with_model, use_reference, use_function,
                 model_reference):
        super().__init__(attribute=attribute_name,
                         with_model=association_model,
                         with_reference=use_reference,
                         with_function=use_function,
                         with_attribute=model_reference,
                         get_association=connect_with_model)
