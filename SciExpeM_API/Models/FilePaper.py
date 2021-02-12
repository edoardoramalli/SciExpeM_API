import SciExpeM_API.Utility.Tools as TL


class FilePaper:
    def __init__(self, id=None):
        self._id = id
        self._title = None
        self._reference_doi = None

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        if not self._title:
            self._title = TL.getProperty('FilePaper', self.id, 'title')
            return self._title
        else:
            return self._title

    @property
    def reference_doi(self):
        if not self._reference_doi:
            self._reference_doi = TL.getProperty('FilePaper', self.id, 'reference_doi')
            return self._reference_doi
        else:
            return self._reference_doi

    @classmethod
    def from_dict(cls, data_dict):
        if isinstance(data_dict, cls):
            return data_dict
        else:
            return cls(**data_dict)

    def refresh(self):
        self._title = None
        self._reference_doi = None

    def serialize(self, exclude=None):
        if exclude is None:
            exclude = []
        diz = dict(self.__dict__)
        diz.pop("id", None)
        for e in exclude:
            diz.pop(e, None)
        return diz

    def __repr__(self):
        return f'<FilePaper ({self.id})>'
