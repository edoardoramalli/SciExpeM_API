import pandas as pd
from .DataColumn import DataColumn
from .FilePaper import FilePaper
from .InitialSpecie import InitialSpecie
from .CommonProperty import CommonProperty
import SciExpeM_API.Utility.Tools as TL
from SciExpeM_API import settings
import json




class Experiment:

    # def __init__(self, reactor=None, experiment_type=None, fileDOI=None,
    #              data_columns=None, initial_species=None, common_properties=None, status=None,
    #              fuels=None,
    #              phi_inf=None, phi_sup=None,
    #              t_inf=None, t_sup=None,
    #              p_inf=None, p_sup=None,
    #              experimentClassifier=None,
    #              file_paper=None,
    #              ignition_type=None, xml_file=None, os_input_file=None, id=None):
    #     self.id = id
    #     self.FilePaper = FilePaper.from_dict(file_paper) if file_paper else None
    #     self.DataColumn = [DataColumn.from_dict(data) for data in data_columns]
    #     self.data_columns_df, self.data_columns_units = self.data_columns_df(self.DataColumn)
    #     self.InitialSpecie = [InitialSpecie.from_dict(data) for data in initial_species]
    #     self.CommonProperty = [CommonProperty.from_dict(data) for data in common_properties]

    def __init__(self, id=None, data_columns=None, file_paper=None,
                 initial_species=None, common_properties=None, refresh=False):
        self._id = id

        # Object
        self._data_columns = TL.optimize(settings.DB, 'DataColumn', json.dumps(data_columns), refresh=refresh)
        self._initial_species = TL.optimize(settings.DB, 'InitialSpecie', json.dumps(initial_species), refresh=refresh)
        self._common_properties = TL.optimize(settings.DB, 'CommonProperty', json.dumps(common_properties), refresh=refresh)
        self._file_paper = TL.optimize(settings.DB, 'FilePaper', json.dumps([file_paper]), refresh=refresh)[0]

        # Simple
        self._experiment_type = None
        self._xml_file = None
        self._reactor = None
        self._fileDOI = None
        self._status = None
        self._ignition_type = None
        self._os_input_file = None
        self._fuels = None
        self._phi_inf = None
        self._phi_sup = None
        self._t_inf = None
        self._t_sup = None
        self._p_inf = None
        self._p_sup = None
        self._experiment_classifier = None

    @property
    def id(self):
        return self._id

    @property
    def experimentClassifier(self):
        if not self._experiment_classifier:
            self._experiment_classifier = TL.getProperty('Experiment', self.id, 'experiment_classifier')
            return self._experiment_classifier
        else:
            return self._experiment_classifier

    @property
    def p_sup(self):
        if not self._p_sup:
            self._p_sup = TL.getProperty('Experiment', self.id, 'p_sup')
            return self._p_sup
        else:
            return self._p_sup

    @property
    def p_inf(self):
        if not self._p_inf:
            self._p_inf = TL.getProperty('Experiment', self.id, 'p_inf')
            return self._p_inf
        else:
            return self._p_inf

    @property
    def t_sup(self):
        if not self._t_sup:
            self._t_sup = TL.getProperty('Experiment', self.id, 't_sup')
            return self._t_sup
        else:
            return self._t_sup

    @property
    def t_inf(self):
        if not self._t_inf:
            self._t_inf = TL.getProperty('Experiment', self.id, 't_inf')
            return self._t_inf
        else:
            return self._t_inf

    @property
    def phi_sup(self):
        if not self._phi_sup:
            self._phi_sup = TL.getProperty('Experiment', self.id, 'phi_sup')
            return self._phi_sup
        else:
            return self._phi_sup

    @property
    def phi_inf(self):
        if not self._phi_inf:
            self._phi_inf = TL.getProperty('Experiment', self.id, 'phi_inf')
            return self._phi_inf
        else:
            return self._phi_inf

    @property
    def fuels(self):
        if not self._fuels:
            self._fuels = TL.getProperty('Experiment', self.id, 'fuels')
            return self._fuels
        else:
            return self._fuels

    @property
    def os_input_file(self):
        if not self._os_input_file:
            self._os_input_file = TL.getProperty('Experiment', self.id, 'os_input_file')
            return self._os_input_file
        else:
            return self._os_input_file

    @property
    def ignition_type(self):
        if not self._ignition_type:
            self._ignition_type = TL.getProperty('Experiment', self.id, 'ignition_type')
            return self._ignition_type
        else:
            return self._ignition_type

    @property
    def status(self):
        if not self._status:
            self._status = TL.getProperty('Experiment', self.id, 'status')
            return self._status
        else:
            return self._status

    @property
    def fileDOI(self):
        if not self._fileDOI:
            self._fileDOI = TL.getProperty('Experiment', self.id, 'fileDOI')
            return self._fileDOI
        else:
            return self._fileDOI

    @property
    def reactor(self):
        if not self._reactor:
            self._reactor = TL.getProperty('Experiment', self.id, 'reactor')
            return self._reactor
        else:
            return self._reactor

    @property
    def experiment_type(self):
        if not self._experiment_type:
            self._experiment_type = TL.getProperty('Experiment', self.id, 'experiment_type')
            return self._experiment_type
        else:
            return self._experiment_type

    @property
    def xml_file(self):
        if not self._xml_file:
            self._xml_file = TL.getProperty('Experiment', self.id, 'xml_file')
            return self._xml_file
        else:
            return self._file_paper

    # --- Object
    @property
    def file_paper(self):
        return self._file_paper

    @property
    def common_properties(self):
        return self._common_properties

    @property
    def initial_species(self):
        return self._initial_species

    @property
    def data_columns(self):
        return self._data_columns

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

    def refresh(self):
        self._experiment_type = None
        self._xml_file = None
        self._reactor = None
        self._fileDOI = None
        self._status = None
        self._ignition_type = None
        self._os_input_file = None
        self._fuels = None
        self._phi_inf = None
        self._phi_sup = None
        self._t_inf = None
        self._t_sup = None
        self._p_inf = None
        self._p_sup = None
        self._experiment_classifier = None

    def __repr__(self):
        return f'<Experiment ({self.id})>'
