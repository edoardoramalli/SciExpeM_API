import SciExpeM_API.Utility.Tools as Tool


class DataColumn:

    def __init__(self, id=None, name=None, units=None, data=None, dg_id=None,
                 label=None, species=None, plotscale=None, ignore=None, nominal=None):
        self._id = id
        self._name = name
        self._units = units
        self._data = data
        self._dg_id = dg_id
        self._label = label
        self._species = species
        self._plotscale = plotscale
        self._ignore = ignore
        self._nominal = nominal

    @property
    def id(self):
        return self._id

    @property
    def data(self):
        if not self._data:
            self._data = Tool.getProperty(self.__class__.__name__, self.id, 'data')
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
    def nominal(self):
        if not self._nominal:
            self._nominal = Tool.getProperty(self.__class__.__name__, self.id, 'nominal')
            return self._nominal
        else:
            return self._nominal

    @property
    def ignore(self):
        if not self._ignore:
            self._ignore = Tool.getProperty(self.__class__.__name__, self.id, 'ignore')
            return self._ignore
        else:
            return self._ignore

    @property
    def plotscale(self):
        if not self._plotscale:
            self._plotscale = Tool.getProperty(self.__class__.__name__, self.id, 'plotscale')
            return self._plotscale
        else:
            return self._plotscale

    @property
    def label(self):
        if not self._label:
            self._label = Tool.getProperty(self.__class__.__name__, self.id, 'label')
            return self._label
        else:
            return self._label

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

    def refresh(self):
        self._name = None
        self._units = None
        self._data = None
        self._dg_id = None
        self._label = None
        self._species = None
        self._plotscale = None
        self._ignore = None
        self._nominal = None

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
