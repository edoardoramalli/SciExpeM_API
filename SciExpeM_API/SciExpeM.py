from SciExpeM_API.Utility.RequestAPI import HTTP_TYPE, RequestAPI
from SciExpeM_API.Utility.Tools import optimize
from SciExpeM_API.Utility.User import User
from SciExpeM_API.Utility import settings
from SciExpeM_API.Views import _ExperimentManager

import os
import json


class SciExpeM(_ExperimentManager):
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

        params = {'status': status, 'exp_id': identifier}

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
                             x_exp: list[float], y_exp: list[float], uncertainty: list[float] = [], verbose=False,
                             **kwargs):

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

    def prova(self, verbose=False):

        params = {'file': open('/Users/edoardo/Documents/GitHub/SciExpeM_API/SciExpeM_API/concentrationProfileExample').read()}

        address = 'ReSpecTh/API/executeOptimaPP'

        request = RequestAPI(ip=self.ip,
                             port=self.port,
                             address=address,
                             token=self.token,
                             mode=HTTP_TYPE.POST,
                             secure=self.secure,
                             params=params)

        if request.requests.status_code == 200:
            if verbose:
                print('ok')

        # response = json.loads((json.loads(request.requests.text)))

        return json.loads(request.requests.text)
