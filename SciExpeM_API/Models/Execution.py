import pandas as pd
import SciExpeM_API.Utility.Tools as TL
from SciExpeM_API import settings
import json


class Execution:

    def __init__(self, chemModel=None, experiment=None, execution_columns=None, id=None):
        self._id = id
        self._chemModel = TL.optimize(settings.DB, 'ChemModel', json.dumps([chemModel]))[0]
        self._Experiment = TL.optimize(settings.DB, 'Experiment', json.dumps([experiment]))[0]
        self._ExecutionColumn = TL.optimize(settings.DB, 'ExecutionColumn', json.dumps(execution_columns))
        # self._execution_columns_df, self.execution_columns_units = self.execution_columns_df(self.ExecutionColumn)
        # self.execution_columns_df = self.execution_columns_df(self.ExecutionColumn)

        self._execution_start = None
        self._execution_end = None

    @property
    def id(self):
        return self._id

    @property
    def execution_start(self):
        if not self._execution_start:
            self._execution_start = TL.getProperty(self.__class__.__name__, self.id, 'execution_start')
            return self._execution_start
        else:
            return self._execution_start

    @property
    def execution_end(self):
        if not self._execution_end:
            self._execution_end = TL.getProperty(self.__class__.__name__, self.id, 'execution_end')
            return self._execution_end
        else:
            return self._execution_end

    @classmethod
    def from_dict(cls, data_dict):
        if isinstance(data_dict, cls):
            return data_dict
        else:
            return cls(**data_dict)

    def __repr__(self):
        return f'<Execution ({self.id})>'

    def execution_columns_df(self, execution_columns_list):
        execution_columns_files = set([])
        for column in execution_columns_list:
            execution_columns_files.add(column.file_type)

        results = {}
        units = {}
        for file in execution_columns_files:
            results[file] = pd.DataFrame()
            units[file] = {}

        for column in execution_columns_list:
            results[column.file_type][column.label] = column.data #, dtype=SI(column.units).units)
            units[column.file_type][column.label] = column.units

        return results, units

    def serialize(self, exclude=None):
        if exclude is None:
            exclude = []
        diz = dict(self.__dict__)
        diz.pop("id", None)
        diz.pop("execution_columns_df", None)
        for e in exclude:
            diz.pop(e, None)
        return diz
