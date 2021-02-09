class CommonProperty:

    def __init__(self, name, units, value, experiment=None, id=None):
        self.id = id
        self.name = name
        self.units = units
        self.value = value
        self.experiment = experiment

    @classmethod
    def from_dict(cls, data_dict):
        if isinstance(data_dict, cls):
            return data_dict
        else:
            return cls(**data_dict)

    def serialize(self, exclude=None):
        if exclude is None:
            exclude = []
        diz = dict(self.__dict__)
        diz.pop("id", None)
        diz.pop("experiment", None)
        for e in exclude:
            diz.pop(e, None)
        return diz

    def __repr__(self):
        return f'<CommonProperty ({self.id})>'
