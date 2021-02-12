import SciExpeM_API.Utility.Tools as TL
from SciExpeM_API import settings
import json


class CurveMatchingResult:

    def __init__(self, id=None, index=None, error=None, execution_column=None, refresh=False):
        self._id = id
        execution = execution_column['execution']
        del execution_column['execution']
        self._execution_column = \
            TL.optimize(settings.DB, 'ExecutionColumn', json.dumps([execution_column]), refresh=refresh)[0]
        self._execution_column.set_execution(
            TL.optimize(settings.DB, 'Execution', json.dumps([execution]), refresh=refresh)[0])
        self._index = index
        self._error = error

    @property
    def id(self):
        return self._id

    @property
    def execution_column(self):
        return self._execution_column

    @property
    def index(self):
        return self._index

    @property
    def error(self):
        return self._error

    @classmethod
    def from_dict(cls, data_dict):
        if isinstance(data_dict, cls):
            return data_dict
        else:
            return cls(**data_dict)

    def refresh(self):
        pass

    def __repr__(self):
        return f'<CurveMatchingResult ({self.id})>'

