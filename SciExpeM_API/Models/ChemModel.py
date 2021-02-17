import SciExpeM_API.Utility.Tools as Tool


class ChemModel:

    def __init__(self, id=None, name=None, xml_file_kinetics=None, xml_file_reaction_names=None, version=None):
        self._id = id
        self._name = name
        self._xml_file_kinetics = xml_file_kinetics
        self._xml_file_reaction_names = xml_file_reaction_names
        self._version = version

    @property
    def id(self):
        return self._id

    @property
    def version(self):
        if not self._version:
            self._version = Tool.getProperty(self.__class__.__name__, self.id, 'version')
            return self._version
        else:
            return self._version


    @property
    def xml_file_reaction_names(self):
        if not self._xml_file_reaction_names:
            self._xml_file_reaction_names = Tool.getProperty(self.__class__.__name__, self.id, 'xml_file_reaction_names')
            return self._xml_file_reaction_names
        else:
            return self._xml_file_reaction_names

    @property
    def xml_file_kinetics(self):
        if not self._xml_file_kinetics:
            self._xml_file_kinetics = Tool.getProperty(self.__class__.__name__, self.id, 'xml_file_kinetics')
            return self._xml_file_kinetics
        else:
            return self._xml_file_kinetics

    @property
    def name(self):
        if not self._name:
            self._name = Tool.getProperty(self.__class__.__name__, self.id, 'name')
            return self._name
        else:
            return self._name

    @classmethod
    def from_dict(cls, data_dict):
        if isinstance(data_dict, cls):
            return data_dict
        else:
            return cls(**data_dict)

    def refresh(self):
        self._name = None
        self._xml_file_kinetics = None
        self._xml_file_reaction_names = None

    def serialize(self):
        return Tool.serialize(self, exclude=['id'])

    def __repr__(self):
        return f'<ChemModel ({self.id})>'
