import SciExpeM_API.Utility.Tools as Tool
from SciExpeM_API.Utility import settings
from .Specie import Specie

import json


class DataColumn:

    def __init__(self, id=None, name=None, units=None, data=None, dg_id=None, source_type=None, label=None,
                 dg_label=None, species=None, uncertainty_reference=None, refresh=False, species_object=None,
                 data_group_profile=None, uncertainty_kind=None, uncertainty_bound=None):
        self._id = id
        self._name = name
        self._units = units
        self._data = data
        self._dg_id = dg_id
        self._dg_label = dg_label
        self._label = label
        self._species = species
        self._source_type = source_type
        self._data_group_profile = data_group_profile
        self._uncertainty_kind = uncertainty_kind
        self._uncertainty_bound = uncertainty_bound

        self._diz = None
        self._is_x = None
        self._is_y = None

        # -- Object

        self._species_object = species_object if Tool.checkListType(species_object, Specie) \
            else Tool.optimize(settings.DB, 'Specie', json.dumps(species_object), refresh=refresh)

        if isinstance(uncertainty_reference, DataColumn):
            self._uncertainty_reference = uncertainty_reference
        else:
            tmp = Tool.optimize(settings.DB, 'DataColumn', json.dumps([uncertainty_reference]), refresh=refresh)
            if tmp:
                self._uncertainty_reference = tmp[0]
            else:
                self._uncertainty_reference = None

    @property
    def diz(self):
        if not self._diz:
            self._diz = {
                'header': self.name if self.name != 'composition' else '+'.join([specie.preferredKey for specie in self.species_object]),
                'units': self.units,
                'data': self.data
            }
            return self._diz
        else:
            return self._diz

    @property
    def id(self):
        return self._id

    @property
    def species_object(self):
        return self._species_object
    
    @property
    def is_x(self):
        if not self._is_x:
            self._is_x = Tool.getProperty(self.__class__.__name__, self.id, 'is_x')
            return self._is_x
        else:
            return self._is_x
    
    @property
    def is_y(self):
        if not self._is_y:
            self._is_y = Tool.getProperty(self.__class__.__name__, self.id, 'is_y')
            return self._is_y
        else:
            return self._is_y

    @property
    def data(self):
        if not self._data:
            self._data = Tool.getProperty(self.__class__.__name__, self.id, 'data')
            return json.loads(self._data)
        else:
            return self._data

    @property
    def species(self):
        if not self._species:
            self._species = Tool.getProperty(self.__class__.__name__, self.id, 'species')
            return self._species
        else:
            return self._species

    @property
    def label(self):
        if not self._label:
            self._label = Tool.getProperty(self.__class__.__name__, self.id, 'label')
            return self._label
        else:
            return self._label

    @property
    def uncertainty_kind(self):
        if not self._uncertainty_kind:
            self._uncertainty_kind = Tool.getProperty(self.__class__.__name__, self.id, 'uncertainty_kind')
            return self._uncertainty_kind
        else:
            return self._uncertainty_kind

    @property
    def uncertainty_bound(self):
        if not self._uncertainty_bound:
            self._uncertainty_bound = Tool.getProperty(self.__class__.__name__, self.id, 'uncertainty_bound')
            return self._uncertainty_bound
        else:
            return self._uncertainty_bound

    @property
    def data_group_profile(self):
        if not self._data_group_profile:
            self._data_group_profile = Tool.getProperty(self.__class__.__name__, self.id, 'data_group_profile')
            return self._data_group_profile
        else:
            return self._data_group_profile

    @property
    def dg_label(self):
        if not self._dg_label:
            self._dg_label = Tool.getProperty(self.__class__.__name__, self.id, 'dg_label')
            return self._dg_label
        else:
            return self._dg_label

    @property
    def dg_id(self):
        if not self._dg_id:
            self._dg_id = Tool.getProperty(self.__class__.__name__, self.id, 'dg_id')
            return self._dg_id
        else:
            return self._dg_id

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
    def source_type(self):
        if not self._source_type:
            self._source_type = Tool.getProperty(self.__class__.__name__, self.id, 'source_type')
            return self._source_type
        else:
            return self._source_type

    # --- Object
    @property
    def uncertainty_reference(self):
        return self._uncertainty_reference

    def refresh(self):
        self._name = None
        self._units = None
        self._data = None
        self._dg_id = None
        self._dg_label = None
        self._label = None
        self._species = None
        self._source_type = None
        self._data_group_profile = None
        self._uncertainty_kind = None
        self._uncertainty_bound = None

    @classmethod
    def from_dict(cls, data_dict):
        if isinstance(data_dict, cls):
            return data_dict
        else:
            return cls(**data_dict)

    def serialize(self):
        return Tool.serialize(self, exclude=['id'])

    def __repr__(self):
        return f'<DataColumns ({self.id})>'
