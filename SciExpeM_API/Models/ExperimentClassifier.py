import SciExpeM_API.Utility.Tools as TL
from SciExpeM_API import settings
import json


class ExperimentClassifier:

    def __init__(self, id=None, mappings=None, rules=None, name=None, model_type=None, solver=None, refresh=False):
        self._id = id
        self._name = name
        self._model_type = model_type
        self._solver = solver
        if type(mappings) == list:
            self._mappings = mappings
        else:
            self._mappings = TL.optimize(settings.DB, 'MappingClassifier', json.dumps(mappings), refresh=refresh)
        if type(rules) == list:
            self._rules = rules
        else:
            self._rules = TL.optimize(settings.DB, 'RuleClassifier', json.dumps(rules), refresh=refresh)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        if not self._name:
            self._name = TL.getProperty(self.__class__.__name__, self.id, 'name')
            return self._name
        else:
            return self._name

    @property
    def solver(self):
        if not self._solver:
            self._solver = TL.getProperty(self.__class__.__name__, self.id, 'solver')
            return self._solver
        else:
            return self._solver

    @property
    def model_type(self):
        if not self._model_type:
            self._model_type = TL.getProperty(self.__class__.__name__, self.id, 'model_type')
            return self._model_type
        else:
            return self._model_type

    @classmethod
    def from_dict(cls, data_dict):
        if isinstance(data_dict, cls):
            return data_dict
        else:
            return cls(**data_dict)

    def refresh(self):
        self._name = None
        self._model_type = None

    def serialize(self):
        return TL.serialize(self, exclude=['id'])

    def __repr__(self):
        return f'<ExperimentClassifier ({self.id})>'
