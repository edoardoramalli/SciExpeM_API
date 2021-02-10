import SciExpeM_API.Utility.Tools as TL


class ChemModel:

    def __init__(self, id=None):
        self._id = id
        self._name = None
        self._xml_file_kinetics = None
        self._xml_file_reaction_names = None

    @property
    def id(self):
        return self._id

    @property
    def xml_file_reaction_names(self):
        if not self._xml_file_reaction_names:
            self._xml_file_reaction_names = TL.getProperty(self.__class__.__name__, self.id, 'xml_file_reaction_names')
            return self._xml_file_reaction_names
        else:
            return self._xml_file_reaction_names

    @property
    def xml_file_kinetics(self):
        if not self._xml_file_kinetics:
            self._xml_file_kinetics = TL.getProperty(self.__class__.__name__, self.id, 'xml_file_kinetics')
            return self._xml_file_kinetics
        else:
            return self._xml_file_kinetics

    @property
    def name(self):
        if not self._name:
            self._name = TL.getProperty(self.__class__.__name__, self.id, 'name')
            return self._name
        else:
            return self._name

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
        for e in exclude:
            diz.pop(e, None)
        return diz

    def __repr__(self):
        return f'<ChemModel ({self.id}) {self.name}>'
