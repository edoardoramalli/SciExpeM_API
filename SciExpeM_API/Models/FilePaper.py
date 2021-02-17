import SciExpeM_API.Utility.Tools as Tool


class FilePaper:
    def __init__(self, id=None, references=None, reference_doi=None):
        self._id = id
        self._references = references
        self._reference_doi = reference_doi

    @property
    def id(self):
        return self._id

    @property
    def references(self):
        if not self._references:
            self._references = Tool.getProperty('FilePaper', self.id, 'references')
            return self._references
        else:
            return self._references

    @property
    def reference_doi(self):
        if not self._reference_doi:
            self._reference_doi = Tool.getProperty('FilePaper', self.id, 'reference_doi')
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
        self._references = None
        self._reference_doi = None

    def serialize(self):
        return Tool.serialize(self, exclude=['id'])

    def __repr__(self):
        return f'<FilePaper ({self.id})>'
