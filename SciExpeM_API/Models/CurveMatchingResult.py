import SciExpeM_API.Utility.Tools as TL


class CurveMatchingResult:

    def __init__(self, id=None):
        self._id = id
        # self.execution_column = ExecutionColumn(**dict(execution_column))
        self._index = None
        self._error = None

    @property
    def id(self):
        return self._id

    @property
    def index(self):
        if not self._index:
            self._index = TL.getProperty(self.__class__.__name__, self.id, 'index')
            return self._index
        else:
            return self._index

    @property
    def error(self):
        if not self._error:
            self._error = TL.getProperty(self.__class__.__name__, self.id, 'error')
            return self._error
        else:
            return self._error

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
