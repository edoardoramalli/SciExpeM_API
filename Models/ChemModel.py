class ChemModel:

    def __init__(self, name, xml_file_kinetics, xml_file_reaction_names, id=None, version=None):
        self.id = id
        self.name = name
        self.xml_file_kinetics = xml_file_kinetics
        self.xml_file_reaction_names = xml_file_reaction_names
        self.version = version

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
