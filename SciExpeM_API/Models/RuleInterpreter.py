import SciExpeM_API.Utility.Tools as Tool


class RuleInterpreter:

    def __init__(self, id=None, model_name=None, property_name=None, property_value=None):
        self._id = id
        self._model_name = model_name
        self._property_name = property_name
        self._property_value = property_value

    @property
    def id(self):
        return self._id

    @property
    def model_name(self):
        if not self._model_name:
            self._model_name = Tool.getProperty(self.__class__.__name__, self.id, 'model_name')
            return self._model_name
        else:
            return self._model_name

    @property
    def property_name(self):
        if not self._property_name:
            self._property_name = Tool.getProperty(self.__class__.__name__, self.id, 'property_name')
            return self._property_name
        else:
            return self._property_name

    @property
    def property_value(self):
        if not self._property_value:
            self._property_value = Tool.getProperty(self.__class__.__name__, self.id, 'property_value')
            return self._property_value
        else:
            return self._property_value

    @classmethod
    def from_dict(cls, data_dict):
        if isinstance(data_dict, cls):
            return data_dict
        else:
            return cls(**data_dict)

    def refresh(self):
        self._model_name = None
        self._property_value = None
        self._property_name = None

    def serialize(self):
        return Tool.serialize(self, exclude=['id'])

    def __repr__(self):
        return f'<RuleInterpreter ({self.id})>'
