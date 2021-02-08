import pandas as pd
from .DataColumn import DataColumn
from .FilePaper import FilePaper
from .InitialSpecie import InitialSpecie
from .CommonProperty import CommonProperty


class Experiment:

    def __init__(self, reactor, experiment_type, fileDOI,
                 data_columns, initial_species, common_properties, status,
                 fuels=None,
                 phi_inf=None, phi_sup=None,
                 t_inf=None, t_sup=None,
                 p_inf=None, p_sup=None,
                 experimentClassifier=None,
                 file_paper=None,
                 ignition_type=None, xml_file=None, os_input_file=None, id=None):
        self.id = id
        self.reactor = reactor
        self.experiment_type = experiment_type
        self.fileDOI = fileDOI
        self.status = status
        self.FilePaper = FilePaper.from_dict(file_paper) if file_paper else None
        self.ignition_type = ignition_type
        self.xml_file = xml_file
        self.os_input_file = os_input_file
        self.DataColumn = [DataColumn.from_dict(data) for data in data_columns]
        self.data_columns_df, self.data_columns_units = self.data_columns_df(self.DataColumn)
        self.InitialSpecie = [InitialSpecie.from_dict(data) for data in initial_species]
        self.CommonProperty = [CommonProperty.from_dict(data) for data in common_properties]
        self.fuels = fuels
        self.phi_inf = phi_inf
        self.phi_sup = phi_sup
        self.t_inf = t_inf
        self.t_sup = t_sup
        self.p_inf = p_inf
        self.p_sup = p_sup
        self.experimentClassifier = experimentClassifier

    def data_columns_df(self, data_columns_list):
        data_columns_group_ids = set([])
        for column in data_columns_list:
            data_columns_group_ids.add(column.dg_id)

        results = {}
        units = {}
        for group_id in data_columns_group_ids:
            results[group_id] = pd.DataFrame()
            units[group_id] = {}

        for column in data_columns_list:
            results[column.dg_id][column.name] = column.data
            units[column.dg_id][column.label] = column.units

        return results, units

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
        diz.pop("data_columns_df", None)
        for e in exclude:
            diz.pop(e, None)
        return diz

    def __repr__(self):
        return f'<Experiment ({self.id}) {self.fileDOI}>'
