import SciExpeM_API.Utility.Tools as Tool
import pandas as pd
from .Species import Species
from SciExpeM_API.Utility import settings
import json


class InitialSpecies:

    def __init__(self, id=None, name=None, units=None, value=None, source_type=None, 
                configuration=None, species=None, refresh=False):
        self._id = id
        self._name = name
        self._units = units
        self._value = value
        self._source_type = source_type
        self._configuration = configuration
        
        self._species = species if isinstance(species, Species) else \
            Tool.optimize(settings.DB, 'Species', json.dumps([species]), refresh=refresh)[0] # TODO: qui mettere species_object??????

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        if not self._name:
            self._name = Tool.getProperty(self.__class__.__name__, self.id, 'name')
            return self._name
        else:
            return self._name

    @property
    def units(self):
        if not self._units:
            self._units = Tool.getProperty(self.__class__.__name__, self.id, 'units')
            return self._units
        else:
            return self._units

    @property
    def value(self):
        if not self._value:
            self._value = Tool.getProperty(self.__class__.__name__, self.id, 'value')
            return self._value
        else:
            return self._value

    @property
    def source_type(self):
        if not self._source_type:
            self._source_type = Tool.getProperty(self.__class__.__name__, self.id, 'source_type')
            return self._source_type
        else:
            return self._source_type

    @property
    def configuration(self):
        if not self._configuration:
            self._configuration = Tool.getProperty(self.__class__.__name__, self.id, 'configuration')
            return self._configuration
        else:
            return self._configuration     

    @classmethod
    def from_dict(cls, data_dict):
        if isinstance(data_dict, cls):
            return data_dict
        else:
            return cls(**data_dict)

    @property
    def species(self):
        return self._species

    def refresh(self):
        self._name = None
        self._units = None
        self._value = None
        self._source_type = None
        self._configuration=None

    def serialize(self):
        return Tool.serialize(self, exclude=['id'])

    def __repr__(self):
        return f'<InitialSpecie ({self.id})>'
