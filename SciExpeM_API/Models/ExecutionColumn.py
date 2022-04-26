import SciExpeM_API.Utility.Tools as Tool
import json

class ExecutionColumn:
    def __init__(self, id=None):
        self._id = id
        self._data = None
        self._species = None
        self._file_type = None
        self._name = None
        self._label = None
        self._units = None
        self._execution = None
        self._is_x = None
        self._is_y = None

    def set_execution(self, execution):
        self._execution = execution

    @property
    def id(self):
        return self._id

    @property
    def execution(self):
        return self._execution

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
            self._data = json.loads(Tool.getProperty(self.__class__.__name__, self.id, 'data'))
            return self._data
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
    def file_type(self):
        if not self._file_type:
            self._file_type = Tool.getProperty(self.__class__.__name__, self.id, 'file_type')
            return self._file_type
        else:
            return self._file_type

    @property
    def label(self):
        if not self._label:
            self._label = Tool.getProperty(self.__class__.__name__, self.id, 'label')
            return self._label
        else:
            return self._label

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

    def refresh(self):
        self._data = None
        self._species = None
        self._file_type = None
        self._name = None
        self._label = None
        self._units = None
        self._execution = None

    @classmethod
    def from_dict(cls, data_dict):
        if isinstance(data_dict, cls):
            return data_dict
        else:
            return cls(**data_dict)

    def __repr__(self):
        return f'<ExecutionColumn ({self.id})>'
