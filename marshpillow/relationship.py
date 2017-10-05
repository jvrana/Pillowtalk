import re


class RelationshipError(Exception):
    """ Generic relationship error """


class Relationship(object):
    delim = "<>"

    def __init__(self, name, search_function, mod1, attr1, mod2, attr2, mod3=None, attr3=None, envelope=False,
                 many=False):
        self.name = name
        self.search_function = search_function
        self.mod1 = mod1
        self.attr1 = attr1
        self.mod2 = mod2
        self.attr2 = attr2
        self.mod3 = mod3
        self.attr3 = attr3
        self.envelope = envelope
        self.many = many

    def _get_function(self):
        if callable(self.search_function):
            return self.search_function
        elif type(self.search_function) is str:
            return getattr(self.mod2, self.search_function)

    def _get_param(self, with_this):
        if self.attr1 in vars(with_this):
            p = object.__getattribute__(with_this, self.attr1)
            if hasattr(p, "__iter__") and self.attr2 in p:
                return p[self.attr2]
            else:
                return p

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
        if self.envelope:
            p = {self.attr2: p}
        r = fxn(p)
        if not type(r) is list:
            r = [r]
        if self.attr3:
            r = [getattr(x, self.attr3) for x in r]
        if not self.many:
            r = r[0]
        return r


class SmartRelationship(Relationship):
    def __init__(self, name, relation_str, envelope=False, many=False):
        fxn, model_attributes = self._parse_relationship_string(relation_str)
        m1, a1 = model_attributes[0]
        m2, a2 = model_attributes[1]
        m3, a3 = None, None
        if len(model_attributes) >= 3:
            m3, a3 = model_attributes[2]
        super().__init__(name, fxn, m1, a1, m2, a2, m3, a3, envelope=envelope, many=many)

    def _parse_relationship_string(self, s):
        m = re.match("(?P<fxn>\w+)\s(?P<rel>.+)", s)
        if m is None:
            raise Exception("Unable to parse relationship. Relations must have the form \"fxn Model1.attr1 {0} "
                            "Model2.attr2\". Found {1}".format(Relationship.delim, s))
        g = m.groupdict()
        fxn = g["fxn"]
        rel = g["rel"]
        tokens = re.split("\s+{0}\s+".format(Relationship.delim), rel)  # split model and attributes
        if len(tokens) > 3 or len(tokens) < 2:
            raise Exception("Unable to parse relationship. Only 2 or 3 way relationships are allowed. Found {"
                            "0}".format(len(tokens)))
        model_attributes = [t.split('.') for t in tokens]
        return fxn, model_attributes


class One(SmartRelationship):
    def __init__(self, name, relation_str):
        super().__init__(name, relation_str, False, False)


class Many(SmartRelationship):
    def __init__(self, name, relation_str):
        super().__init__(name, relation_str, True, True)
