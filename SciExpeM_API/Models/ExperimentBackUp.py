import SciExpeM_API.Utility.Tools as Tool
from SciExpeM_API.Utility import settings
import json

class ExperimentBackUp:
    def __init__(self, id=None, chemModel=None, experiment=None, dateTime=None, parameter_name=None,
                 parameter_value=None, parameter_unit=None, path=None, refresh=False):

        self._chemModel = Tool.optimize(settings.DB, 'ChemModel', json.dumps([chemModel]), refresh=refresh)[0]
        self._experiment = Tool.optimize(settings.DB, 'Experiment', json.dumps([experiment]), refresh=refresh)[0]

        self._id = id
        self._dateTime = dateTime
        self._parameter_name = parameter_name

        self._parameter_value = parameter_value
        self._parameter_unit = parameter_unit
        self._path = path


    @property
    def id(self):
        return self._id

    @property
    def dateTime(self):
        if not self._dateTime:
            self._dateTime = Tool.getProperty(self.__class__.__name__, self.id, 'dateTime')
            return self._dateTime
        else:
            return self._dateTime

    @property
    def parameter_name(self):
        if not self._parameter_name:
            self._parameter_name = Tool.getProperty(self.__class__.__name__, self.id, 'parameter_name')
            return self._parameter_name
        else:
            return self._parameter_name

    @property
    def parameter_value(self):
        if not self._parameter_value:
            self._parameter_value = Tool.getProperty(self.__class__.__name__, self.id, 'parameter_value')
            return self._parameter_value
        else:
            return self._parameter_value

    @property
    def parameter_unit(self):
        if not self._parameter_unit:
            self._parameter_unit = Tool.getProperty(self.__class__.__name__, self.id, 'parameter_unit')
            return self._parameter_unit
        else:
            return self._parameter_unit

    @property
    def path(self):
        if not self._path:
            self._path = Tool.getProperty(self.__class__.__name__, self.id, 'path')
            return self._path
        else:
            return self._path

    @classmethod
    def from_dict(cls, data_dict):
        if isinstance(data_dict, cls):
            return data_dict
        else:
            return cls(**data_dict)

    def refresh(self):
        self._description = None
        self._reference_doi = None
        self._author = None
        self._year = None
        self._title = None
        self._journal = None
        self._volume = None
        self._page = None

    def serialize(self):
        return Tool.serialize(self, exclude=['id'])

    def __repr__(self):
        return f'<ExperimentBackUp ({self.id})>'
