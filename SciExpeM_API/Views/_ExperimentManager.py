from SciExpeM_API.Utility.QSerializer import QSerializer
from SciExpeM_API.Utility.RequestAPI import HTTP_TYPE, RequestAPI
from SciExpeM_API.Utility.Tools import optimize

from django.db.models import Q

import json
import os


class _ExperimentManager(object):
    def filterDatabase(self, model_name: str, verbose=False, query=None, refresh=False, *args, **kwargs) -> list:
        q_serializer = QSerializer()

        q = q_serializer.dumps(query) if query else q_serializer.dumps(Q(*args, **kwargs))

        params = {'model_name': model_name, 'query': q}

        address = 'ExperimentManager/API/filterDataBase'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.status_code != 200:
            return []
        else:
            if verbose:
                print("Filter Request Successful.")
            return optimize(self, model_name, request.requests.text, refresh)

    def loadExperiment(self, path, format_file, verbose=False):
        if not os.path.isfile(path):
            raise FileNotFoundError(path)

        params = {'format_file': format_file, 'file_text': open(path, 'r').read()}

        address = 'ExperimentManager/API/loadExperiment'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print(json.loads(request.requests.text))

    def updateElement(self, element, model_name: str = None, verbose=False, **kwargs):
        if type(element) == int and not model_name:
            raise Exception("Modal name is not specified.")

        identifier = element if type(element) == int else element.id
        name = model_name if type(element) == int else element.__class__.__name__

        params = {'model_name': name, 'property_dict': json.dumps(kwargs), 'element_id': identifier}

        address = 'ExperimentManager/API/updateElement'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print(json.loads(request.requests.text))

    def insertElement(self, obj=None, verbose=False):

        params = {'model_name': obj.__class__.__name__,'property_dict': json.dumps(obj.serialize())}

        address = 'ExperimentManager/API/insertElement'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print(json.loads(request.requests.text))

    def insertJson(self, json_object, verbose=False):

        params = {'model_name': 'Experiment', 'property_dict': json.dumps(json_object)}

        address = 'ExperimentManager/API/insertElement'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print(json.loads(request.requests.text))

    def deleteElement(self, element, model_name: str = None, verbose=False):
        if type(element) == int and not model_name:
            raise Exception("Modal name is not specified.")

        identifier = element if type(element) == int else element.id
        name = model_name if type(element) == int else element.__class__.__name__

        params = {'model_name': name, 'element_id': identifier}

        address = 'ExperimentManager/API/deleteElement'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print(json.loads(request.requests.text))

    def getCurveMatching(self, experiment: list, verbose=False):
        experiment_id = experiment if type(experiment[0]) == int else [exp.id for exp in experiment]
        params = {'exp_id': experiment_id}

        address = 'ExperimentManager/API/getCurveMatching'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print('Get Curve Matching executed successfully.')

        return json.loads(request.requests.text)

    def getSimulation(self, experiment, verbose=False):
        experiment_id = experiment if type(experiment) == int else experiment.id
        params = {'exp_id': experiment_id}

        address = 'ExperimentManager/API/getSimulation'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print('Get Simulation executed successfully.')

        return json.loads(request.requests.text)
