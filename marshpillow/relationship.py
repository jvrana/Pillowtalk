import re

class Relationship(object):
    def __init__(self, attribute, with_model, with_reference, with_function, with_attribute=None, get_association=None):
        self.attribute = attribute
        self.with_model = with_model
        self.with_reference = with_reference  # e.g. {"id": "address_id"} <> address.id = other_thing.address_id
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
            return object.__getattribute__(this, self.with_reference)
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

class Relation(Relationship):
    def __init__(self, name, fxn, m1, a1, m2, a2, m3=None, a3=None, env=False, many=False):
        self.name = name
        self.fxn = fxn
        self.m1 = m1
        self.a1 = a1
        self.m2 = m2
        self.a2 = a2
        self.m3 = m3
        self.a3 = a3
        self.env = env
        self.many = many

    def _get_function(self):
        if callable(self.fxn):
            return self.fxn
        elif type(self.fxn) is str:
            return getattr(self.m2, self.fxn)

    def _get_param(self, with_this):
        if self.a1 in vars(with_this):
            p = object.__getattribute__(with_this, self.a1)
            if hasattr(p, "__iter__") and self.a2 in p:
                return p[self.a2]
            else:
                return p

    #
    # @property
    # def with_model(self):
    #     return self.m2
    #
    # @with_model.setter
    # def with_model(self, x):
    #     self.m2 = x
    #
    # @property
    # def attribute(self):
    #     return self.name
    #
    # @property
    # def with_reference(self):
    #     return self.a1


    def fullfill(self, with_this):
        """
        find BudgetAssociation.person_id <> Person.id
           Person.find(this.person_id)

        where Person.id <> Email.person_id
           Email.where( {"person_id": this.id} )

        where Person.id <> BudgetAssociation.person_id THEN BudgetAssociation.budget
        BudgetAssociation.where( {"person_id": this.id } )
        for each ba:
            return bs.budget
        """
        fxn = self._get_function()
        p = self._get_param(with_this)
        if self.env:
            p = {self.a2: p}
        r = fxn(p)
        if not type(r) is list:
            r = [r]
        if self.a3:
            r = [getattr(x, self.a3) for x in r]
        if not self.many:
            r = r[0]
        return r

class SmartRelation(Relation):
    def __init__(self, name, relation_str, env=False, many=False):
        fxn, m1, a1, m2, a2, m3, a3 = self._parse_relationship_string(relation_str)
        super().__init__(name, fxn, m1, a1, m2, a2, m3, a3, env=env, many=many)

    def _parse_relationship_string(self, s):
        """
# Association("budgets", "BudgetAssociation", "Budget", "where Person.id <>
BudgetAssociation.person_id AND BudgetAssociation.budget_id <> Budget.id"
# HasMany("emails", "Email", "where Person.id <> Email.person_id"
# HasOne("person" "Person", "find BudgetAssociation.person_id <> Person.id")
"""
        m = re.match("(?P<function>\w+)\s(?P<relation>.+)", s)
        print(s)
        g = m.groupdict()
        relation = g["relation"]
        delim = "<>"
        tokens = re.split("\s+{0}\s+".format(delim), relation)
        model_attribute = [t.split('.') for t in tokens]
        m1, a1 = model_attribute[0]
        m2, a2 = model_attribute[1]
        m3, a3 = None, None
        if len(model_attribute) == 3:
            m3, a3 = model_attribute[2]
        return g["function"], m1, a1, m2, a2, m3, a3

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
