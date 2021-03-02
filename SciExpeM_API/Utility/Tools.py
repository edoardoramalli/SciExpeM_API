import SciExpeM_API.Utility.settings as settings
import SciExpeM_API.Utility.RequestAPI as rAPI
from SciExpeM_API.Models import *
import json


def getProperty(model_name, element_id, property_name):
    params = {'model_name': model_name, 'element_id': element_id, 'property_name': property_name}

    address = 'ExperimentManager/API/requestProperty'

    request = rAPI.RequestAPI(ip=settings.IP,
                              port=settings.PORT,
                              address=address,
                              token=settings.TOKEN,
                              mode=rAPI.HTTP_TYPE.POST,
                              secure=settings.SECURE,
                              params=params)
    return json.loads(request.requests.text) if json.loads(request.requests.text) != '' else None


def optimize(database, model_name, text, refresh=False):
    model = eval(model_name)
    refresh_models = ['CurveMatchingResult', 'Execution', 'Experiment']
    if model in refresh_models:
        text['refresh'] = refresh
    tmp = [model.from_dict(element) for element in json.loads(text)]
    result = []

    for element in tmp:
        attribute = getattr(database, model_name)
        if element.id in attribute:
            result.append(attribute[element.id])
            if refresh:
                attribute[element.id].refresh()
        else:
            attribute[element.id] = element
            result.append(element)
    return result


def serialize(obj, exclude):
    if exclude is None:
        exclude = []
    diz = {key.replace('_', '', 1) if key.startswith('_') else key: value for key, value in dict(obj.__dict__).items()}
    for e in exclude:
        diz.pop(e, None)
    tmp = {}
    for key, value in diz.items():
        if type(value) == list:
            tmp[key] = [x.serialize() if not isinstance(x, int) else x for x in value]
        else:
            if isinstance(value, FilePaper):
                tmp[key] = value.serialize()
            else:
                tmp[key] = value
    # diz = {key: [x.serialize() if not isinstance(x, int) else x for x in value] if type(value) == list else value for key, value in diz.items()}

    return tmp


def checkListType(obj, check_type):
    return all(isinstance(x, check_type) for x in obj)
