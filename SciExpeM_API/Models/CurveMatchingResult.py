import SciExpeM_API.Utility.Tools as Tool
from SciExpeM_API.Utility import settings
import json


class CurveMatchingResult:

    def __init__(self, id=None, score=None, error=None, execution_column=None, refresh=False):
        self._id = id
        execution = execution_column['execution']
        del execution_column['execution']
        self._execution_column = \
            Tool.optimize(settings.DB, 'ExecutionColumn', json.dumps([execution_column]), refresh=refresh)[0]
        self._execution_column.set_execution(
            Tool.optimize(settings.DB, 'Execution', json.dumps([execution]), refresh=refresh)[0])
        self._score = score
        self._error = error

    @property
    def id(self):
        return self._id

    @property
    def execution_column(self):
        return self._execution_column

    @property
    def error(self):
        return self._error

    @property
    def score(self):
        return self._score

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

