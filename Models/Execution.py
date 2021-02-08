import pandas as pd
from . import Experiment, ExecutionColumn


class Execution:

    def __init__(self, chemModel, experiment, execution_columns, execution_start=None, execution_end=None, id=None):
        self.id = id
        self.chemModel = chemModel
        self.Experiment = Experiment(**dict(experiment))
        self.execution_start = execution_start
        self.execution_end = execution_end
        self.ExecutionColumn = [ExecutionColumn.ExecutionColumn.from_dict(data) for data in execution_columns]
        self.execution_columns_df, self.execution_columns_units = self.execution_columns_df(self.ExecutionColumn)
        # self.execution_columns_df = self.execution_columns_df(self.ExecutionColumn)

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
