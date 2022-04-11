import SciExpeM_API.Utility.Tools as Tool


class Specie:
    def __init__(self,
                 id=None, InChI=None, preferredKey=None, formula=None, names=None, CAS=None, SMILES=None,
                 chemName=None):
        self._id = id
        self._InChI = InChI
        self._preferredKey = preferredKey

        self._formula = formula
        self._names = names
        self._CAS = CAS
        self._SMILES = SMILES
        self._chemName = chemName


    @property
    def id(self):
        return self._id

    @property
    def InChI(self):
        if not self._InChI:
            self._InChI = Tool.getProperty('Specie', self.id, 'InChI')
            return self._InChI
        else:
            return self._InChI

    @property
    def preferredKey(self):
        if not self._preferredKey:
            self._preferredKey = Tool.getProperty('Specie', self.id, 'preferredKey')
            return self._preferredKey
        else:
            return self._preferredKey

    @property
    def formula(self):
        if not self._formula:
            self._formula = Tool.getProperty('Specie', self.id, 'formula')
            return self._formula
        else:
            return self._formula

    @property
    def names(self):
        if not self._names:
            self._names = Tool.getProperty('Specie', self.id, 'names')
            return self._names
        else:
            return self._names

    @property
    def CAS(self):
        if not self._CAS:
            self._CAS = Tool.getProperty('Specie', self.id, 'CAS')
            return self._CAS
        else:
            return self._CAS

    @property
    def SMILES(self):
        if not self._SMILES:
            self._SMILES = Tool.getProperty('Specie', self.id, 'SMILES')
            return self._SMILES
        else:
            return self._SMILES

    @property
    def chemName(self):
        if not self._chemName:
            self._chemName = Tool.getProperty('Specie', self.id, 'chemName')
            return self._chemName
        else:
            return self._chemName

    @classmethod
    def from_dict(cls, data_dict):
        if isinstance(data_dict, cls):
            return data_dict
        else:
            return cls(**data_dict)

    def refresh(self):
        self._InChI = None
        self._preferredKey = None

        self._formula = None
        self._names = None
        self._CAS = None
        self._SMILES = None
        self._chemName = None

    def serialize(self):
        return Tool.serialize(self, exclude=['id'])

    def __repr__(self):
        return f'<Specie ({self.id})>'
