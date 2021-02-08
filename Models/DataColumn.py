# import pint_pandas
# from pint import UnitRegistry


# SI = UnitRegistry()
# SI.load_definitions('units.def')
# PA_ = pint_pandas.PintArray
# pint_pandas.PintType.ureg = SI

class DataColumn:

    def __init__(self, name, units, data, dg_id,
                 plotscale, ignore, nominal=None, label=None, experiment=None, species=None, id=None):
        self.id = id
        self.name = name
        self.units = units
        self.data = data
        self.dg_id = dg_id
        self.label = label
        self.species = species
        self.experiment = experiment
        self.plotscale = plotscale
        self.ignore = ignore
        self.nominal = nominal

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
        diz.pop("experiment", None)
        for e in exclude:
            diz.pop(e, None)
        return diz

    def __repr__(self):
        return f'<DataColumns ({self.id})>'
