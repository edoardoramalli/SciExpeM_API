class FilePaper:
    def __init__(self, title, reference_doi=None, id=None):
        self.id = id
        self.title = title
        self.reference_doi = reference_doi

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
        return f'<FilePaper ({self.id})>'
