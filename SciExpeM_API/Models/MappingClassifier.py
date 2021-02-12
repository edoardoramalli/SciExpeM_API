import SciExpeM_API.Utility.Tools as TL


class MappingClassifier:

    def __init__(self, id=None, file=None,
                 x_exp_name=None, x_exp_location=None, x_sim_name=None, x_sim_location=None,
                 y_exp_name=None, y_exp_location=None, y_sim_name=None, y_sim_location=None):
        self._id = id

        self._x_exp_name = x_exp_name
        self._x_exp_location = x_exp_location
        self._x_sim_name = x_sim_name
        self._x_sim_location = x_sim_location

        self._y_exp_name = y_exp_name
        self._y_exp_location = y_exp_location
        self._y_sim_name = y_sim_name
        self._y_sim_location = y_sim_location

        self._file = file

    @property
    def id(self):
        return self._id

    @property
    def x_exp_name(self):
        if not self._x_exp_name:
            self._x_exp_name = TL.getProperty(self.__class__.__name__, self.id, 'x_exp_name')
            return self._x_exp_name
        else:
            return self._x_exp_name

    @property
    def x_exp_location(self):
        if not self._x_exp_location:
            self._x_exp_location = TL.getProperty(self.__class__.__name__, self.id, 'x_exp_location')
            return self._x_exp_location
        else:
            return self._x_exp_location

    @property
    def x_sim_name(self):
        if not self._x_sim_name:
            self._x_sim_name = TL.getProperty(self.__class__.__name__, self.id, 'x_sim_name')
            return self._x_sim_name
        else:
            return self._x_sim_name

    @property
    def x_sim_location(self):
        if not self._x_sim_location:
            self._x_sim_location = TL.getProperty(self.__class__.__name__, self.id, 'x_sim_location')
            return self._x_sim_location
        else:
            return self._x_sim_location

    @property
    def y_exp_name(self):
        if not self._y_exp_name:
            self._y_exp_name = TL.getProperty(self.__class__.__name__, self.id, 'y_exp_name')
            return self._y_exp_name
        else:
            return self._y_exp_name

    @property
    def y_exp_location(self):
        if not self._y_exp_location:
            self._y_exp_location = TL.getProperty(self.__class__.__name__, self.id, 'y_exp_location')
            return self._y_exp_location
        else:
            return self._y_exp_location

    @property
    def y_sim_name(self):
        if not self._y_sim_name:
            self._y_sim_name = TL.getProperty(self.__class__.__name__, self.id, 'y_sim_name')
            return self._y_sim_name
        else:
            return self._y_sim_name

    @property
    def y_sim_location(self):
        if not self._y_sim_location:
            self._y_sim_location = TL.getProperty(self.__class__.__name__, self.id, 'y_sim_location')
            return self._y_sim_location
        else:
            return self._y_sim_location

    @property
    def file(self):
        if not self._file:
            self._file = TL.getProperty(self.__class__.__name__, self.id, 'file')
            return self._file
        else:
            return self._file

    @classmethod
    def from_dict(cls, data_dict):
        if isinstance(data_dict, cls):
            return data_dict
        else:
            return cls(**data_dict)

    def refresh(self):
        self._file = None
        self._x_exp_name = None
        self._x_exp_location = None
        self._x_sim_name = None
        self._x_sim_location = None

        self._y_exp_name = None
        self._y_exp_location = None
        self._y_sim_name = None
        self._y_sim_location = None


    def serialize(self):
        return TL.serialize(self, exclude=['id'])

    def __repr__(self):
        return f'<MappingClassifier ({self.id})>'
