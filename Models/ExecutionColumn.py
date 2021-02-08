from . import Execution


class ExecutionColumn:
    def __init__(self, data, units, label, file_type, species=None, execution=None, name=None, id=None):
        self.name = name
        self.label = label
        self.units = units
        self.id = id
        self.data = data
        if type(execution) is int:
            self.execution = execution
        elif type(execution) is dict:
            self.execution = Execution(**dict(execution))
        self.species = species
        self.file_type = file_type

    @classmethod
    def from_dict(cls, data_dict):
        if isinstance(data_dict, cls):
            return data_dict
        else:
            return cls(**data_dict)

    def __repr__(self):
        return f'<ExecutionColumn ({self.id})>'

    def serialize(self, exclude=None):
        if exclude is None:
            exclude = []
        diz = dict(self.__dict__)
        diz.pop("id", None)
        diz.pop("execution", None)
        for e in exclude:
            diz.pop(e, None)
        return diz
