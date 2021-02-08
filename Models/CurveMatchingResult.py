from . import ExecutionColumn


class CurveMatchingResult:

    def __init__(self, index, error, id=None):
        self.id = id
        # self.execution_column = ExecutionColumn(**dict(execution_column))
        self.index = index
        self.error = error

    @classmethod
    def from_dict(cls, data_dict):
        if isinstance(data_dict, cls):
            return data_dict
        else:
            return cls(**data_dict)

    def __repr__(self):
        return f'<CurveMatchingResult ({self.id})>'

    def serialize(self, exclude=None):
        if exclude is None:
            exclude = []
        diz = dict(self.__dict__)
        diz.pop("id", None)
        for e in exclude:
            diz.pop(e, None)
        return diz
