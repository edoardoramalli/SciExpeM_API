import SciExpeM_API.Utility.Tools as Tool


class FilePaper:
    def __init__(self, id=None, description=None, reference_doi=None, author=None, title=None, year=None, volume=None,
                 page=None, journal=None):
        self._id = id
        self._description = description
        self._reference_doi = reference_doi

        self._author = author
        self._title = title
        self._year = year
        self._volume = volume
        self._page = page
        self._journal = journal

    @property
    def id(self):
        return self._id

    @property
    def description(self):
        if not self._description:
            self._description = Tool.getProperty('FilePaper', self.id, 'description')
            return self._description
        else:
            return self._description

    @property
    def reference_doi(self):
        if not self._reference_doi:
            self._reference_doi = Tool.getProperty('FilePaper', self.id, 'reference_doi')
            return self._reference_doi
        else:
            return self._reference_doi

    @property
    def year(self):
        if not self._year:
            self._year = Tool.getProperty('FilePaper', self.id, 'year')
            return self._year
        else:
            return self._year

    @property
    def journal(self):
        if not self._journal:
            self._journal = Tool.getProperty('FilePaper', self.id, 'journal')
            return self._journal
        else:
            return self._journal

    @property
    def title(self):
        if not self._title:
            self._title = Tool.getProperty('FilePaper', self.id, 'title')
            return self._title
        else:
            return self._title

    @property
    def page(self):
        if not self._page:
            self._page = Tool.getProperty('FilePaper', self.id, 'page')
            return self._page
        else:
            return self._page

    @property
    def volume(self):
        if not self._volume:
            self._volume = Tool.getProperty('FilePaper', self.id, 'volume')
            return self._volume
        else:
            return self._volume

    @property
    def author(self):
        if not self._author:
            self._author = Tool.getProperty('FilePaper', self.id, 'author')
            return self._author
        else:
            return self._author

    @classmethod
    def from_dict(cls, data_dict):
        if isinstance(data_dict, cls):
            return data_dict
        else:
            return cls(**data_dict)

    def refresh(self):
        self._description = None
        self._reference_doi = None
        self._author = None
        self._year = None
        self._title = None
        self._journal = None
        self._volume = None
        self._page = None

    def serialize(self):
        return Tool.serialize(self, exclude=['id'])

    def __repr__(self):
        return f'<FilePaper ({self.id})>'
