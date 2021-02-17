from SciExpeM_API.Utility.QSerializer import QSerializer
from django.db.models import Q
from .Utility.RequestAPI import HTTP_TYPE, RequestAPI
from .Utility.Tools import optimize
from .Utility.User import User
from SciExpeM_API.Utility import settings

import os
import json


class SciExpeM(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is not None:
            print("Attention. SciExpeM is a singleton.")
            return cls.__instance
        else:
            return object.__new__(cls)

    def __init__(self, ip: str = 'sciexpem.chem.polimi.it',
                 port: int = '443',
                 secure: bool = True,
                 token: str = None, username: str = None, password: str = None):

        SciExpeM.__instance = self
        self.ip = ip
        self.port = port
        self.secure = secure

        if not (username and password) and not token:
            raise Exception("Missing username and password or access token.")
        elif token:
            self.token = token
        elif username and password:
            try:
                self.user = self.getUserInfo(username, password)
            except Exception:
                raise Exception("Authentication failed.")
            self.token = self.user.token

        settings.IP = self.ip
        settings.PORT = self.port
        settings.SECURE = self.secure
        settings.DB = self
        settings.TOKEN = self.token

        self.Experiment = {}
        self.ChemModel = {}
        self.CommonProperty = {}
        self.CurveMatchingResult = {}
        self.DataColumn = {}
        self.Execution = {}
        self.ExecutionColumn = {}
        self.FilePaper = {}
        self.InitialSpecie = {}
        self.ExperimentInterpreter = {}
        self.MappingInterpreter = {}
        self.RuleInterpreter = {}

    def getUserInfo(self, username: str, password: str):

        params = {'username': username, 'password': password}

        address = 'getInfoUser'

        request = RequestAPI(ip=self.ip,
                             port=self.port,
                             address=address,
                             mode=HTTP_TYPE.POST,
                             secure=self.secure,
                             params=params)

        if request.requests.status_code != 200:
            raise Exception()
        else:
            return User(**dict(json.loads(request.requests.text)))

    def filterDatabase(self, model_name: str, verbose=False, query=None, refresh=False, *args, **kwargs) -> list:
        q_serializer = QSerializer()

        q = q_serializer.dumps(query) if query else q_serializer.dumps(Q(*args, **kwargs))

        params = {'model_name': model_name, 'query': q}

        address = 'ExperimentManager/API/filterDataBase'

        request = RequestAPI(ip=self.ip,
                             port=self.port,
                             address=address,
                             token=self.token,
                             mode=HTTP_TYPE.POST,
                             secure=self.secure,
                             params=params)

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

        request = RequestAPI(ip=self.ip,
                             port=self.port,
                             address=address,
                             token=self.token,
                             mode=HTTP_TYPE.POST,
                             secure=self.secure,
                             params=params)

        if request.requests.status_code == 200:
            if verbose:
                print(json.loads(request.requests.text))

    def updateElement(self, element, model_name: str = None, verbose=False, **kwargs):
        if type(element) == int and not model_name:
            raise Exception("Modal name is not specified.")

        identifier = element if type(element) == int else element.id
        name = model_name if type(element) == int else element.__class__.__name__

        params = {'model_name': name, 'property': json.dumps(kwargs), 'id': identifier}

        address = 'ExperimentManager/API/updateElement'

        request = RequestAPI(ip=self.ip,
                             port=self.port,
                             address=address,
                             token=self.token,
                             mode=HTTP_TYPE.POST,
                             secure=self.secure,
                             params=params)

        if request.requests.status_code == 200:
            if verbose:
                print(json.loads(request.requests.text))

    def convertList(self, data_list: list, unit: str, desired_unit: str, verbose: bool = False) -> list:

        params = {'list': data_list, 'unit': unit, 'desired_unit': desired_unit}

        address = 'ReSpecTh/API/convertList'

        request = RequestAPI(ip=self.ip,
                             port=self.port,
                             address=address,
                             token=self.token,
                             mode=HTTP_TYPE.POST,
                             secure=self.secure,
                             params=params)

        if request.requests.status_code == 200:
            if verbose:
                print("List conversion successful.")

        return json.loads(request.requests.text)

    def verifyExperiment(self, experiment, status: str, verbose=False):

        identifier = experiment if type(experiment) == int else experiment.id

        params = {'status': status, 'id': identifier}

        address = 'ExperimentManager/API/verifyExperiment'

        request = RequestAPI(ip=self.ip,
                             port=self.port,
                             address=address,
                             token=self.token,
                             mode=HTTP_TYPE.POST,
                             secure=self.secure,
                             params=params)

        if request.requests.status_code == 200:
            if verbose:
                print(json.loads(request.requests.text))

    def insertElement(self, obj, verbose=False):

        params = {'model_name': obj.__class__.__name__, 'property': json.dumps(obj.serialize())}

        address = 'ExperimentManager/API/insertElement'

        request = RequestAPI(ip=self.ip,
                             port=self.port,
                             address=address,
                             token=self.token,
                             mode=HTTP_TYPE.POST,
                             secure=self.secure,
                             params=params)

        if request.requests.status_code == 200:
            if verbose:
                print(json.loads(request.requests.text))

    def deleteElement(self, element, model_name: str = None, verbose=False):
        if type(element) == int and not model_name:
            raise Exception("Modal name is not specified.")

        identifier = element if type(element) == int else element.id
        name = model_name if type(element) == int else element.__class__.__name__

        params = {'model_name': name, 'id': identifier}

        address = 'ExperimentManager/API/deleteElement'

        request = RequestAPI(ip=self.ip,
                             port=self.port,
                             address=address,
                             token=self.token,
                             mode=HTTP_TYPE.POST,
                             secure=self.secure,
                             params=params)

        if request.requests.status_code == 200:
            if verbose:
                print(json.loads(request.requests.text))

    def startSimulation(self, experiment, chemModel, verbose=False):
        experiment_id = experiment if type(experiment) == int else experiment.id
        chemModel_id = chemModel if type(chemModel) == int else chemModel.id

        params = {'experiment': experiment_id, 'chemModel': chemModel_id}

        address = 'OpenSmoke/API/startSimulation'

        request = RequestAPI(ip=self.ip,
                             port=self.port,
                             address=address,
                             token=self.token,
                             mode=HTTP_TYPE.POST,
                             secure=self.secure,
                             params=params)

        if request.requests.status_code == 200:
            if verbose:
                print(json.loads(request.requests.text))

    def executeCurveMatching(self, x_sim: list[float], y_sim: list[float],
                             x_exp: list[float], y_exp: list[float], uncertainty: list[float] = [],
                             verbose=False, **kwargs):

        params = {'x_sim': x_sim, 'y_sim': y_sim,
                  'x_exp': x_exp, 'y_exp': y_exp,
                  'uncertainty': json.dumps(uncertainty),
                  'configuration': json.dumps(kwargs if kwargs else {})}

        address = 'CurveMatching/API/executeCurveMatching'

        request = RequestAPI(ip=self.ip,
                             port=self.port,
                             address=address,
                             token=self.token,
                             mode=HTTP_TYPE.POST,
                             secure=self.secure,
                             params=params)

        if request.requests.status_code == 200:
            if verbose:
                print('Curve Matching executed successfully.')

        response = json.loads((json.loads(request.requests.text)))

        return response['score'], response['error']
