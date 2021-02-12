import SciExpeM_API.Utility.Tools as TL


class DataColumn:

    def __init__(self, id=None):
        self._id = id
        self._name = None
        self._units = None
        self._data = None
        self._dg_id = None
        self._label = None
        self._species = None
        self._plotscale = None
        self._ignore = None
        self._nominal = None

        # self._experiment = experiment

    @property
    def id(self):
        return self._id

    @property
    def data(self):
        if not self._data:
            self._data = TL.getProperty(self.__class__.__name__, self.id, 'data')
            return self._data
        else:
            return self._data

    @property
    def species(self):
        if not self._species:
            self._species = TL.getProperty(self.__class__.__name__, self.id, 'species')
            return self._species
        else:
            return self._species

    @property
    def nominal(self):
        if not self._nominal:
            self._nominal = TL.getProperty(self.__class__.__name__, self.id, 'nominal')
            return self._nominal
        else:
            return self._nominal

    @property
    def ignore(self):
        if not self._ignore:
            self._ignore = TL.getProperty(self.__class__.__name__, self.id, 'ignore')
            return self._ignore
        else:
            return self._ignore

    @property
    def plotscale(self):
        if not self._plotscale:
            self._plotscale = TL.getProperty(self.__class__.__name__, self.id, 'plotscale')
            return self._plotscale
        else:
            return self._plotscale

    @property
    def label(self):
        if not self._label:
            self._label = TL.getProperty(self.__class__.__name__, self.id, 'label')
            return self._label
        else:
            return self._label

    @property
    def dg_id(self):
        if not self._dg_id:
            self._dg_id = TL.getProperty(self.__class__.__name__, self.id, 'dg_id')
            return self._dg_id
        else:
            return self._dg_id

    @property
    def name(self):
        if not self._name:
            self._name = TL.getProperty(self.__class__.__name__, self.id, 'name')
            return self._name
        else:
            return self._name

    @property
    def units(self):
        if not self._units:
            self._units = TL.getProperty(self.__class__.__name__, self.id, 'units')
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

    def serialize(self, exclude=None):
        if exclude is None:
            exclude = []
        diz = dict(self.__dict__)
        diz.pop("id", None)
        diz.pop("experiment", None)
        for e in exclude:
            diz.pop(e, None)
        return diz

    def __repr__(self):
        return f'<DataColumns ({self.id})>'
