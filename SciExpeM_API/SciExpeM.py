from SciExpeM_API.Utility.RequestAPI import HTTP_TYPE, RequestAPI
from SciExpeM_API.Utility.Tools import optimize
from SciExpeM_API.Utility.User import User
from SciExpeM_API.Utility import settings
from SciExpeM_API.Views import _ExperimentManager, _ReSpecTh, _OpenSmoke

import os
import json


class SciExpeM(_ExperimentManager, _ReSpecTh, _OpenSmoke):
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
                 token: str = None, username: str = None, password: str = None, verify: bool = True,
                 warning: bool = True):

        SciExpeM.__instance = self
        self.ip = ip
        self.port = port
        self.secure = secure
        self.verify = verify

        settings.IP = self.ip
        settings.PORT = self.port
        settings.SECURE = self.secure
        settings.VERIFY = self.verify
        settings.DB = self

        if not warning:
            import requests.packages.urllib3 as W
            W.disable_warnings()

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
        self.Specie = {}

    def getUserInfo(self, username: str, password: str):

        params = {'username': username, 'password': password}

        address = 'getInfoUser'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code != 200:
            raise Exception()
        else:
            return User(**dict(json.loads(request.requests.text)))


    def testConnection(self, verbose=False):

        address = 'testConnection'

        request = RequestAPI(address=address, mode=HTTP_TYPE.GET, params={})

        if request.requests.status_code != 200:
            raise Exception('BOH')
        else:
            if verbose:
                print('Connection OK')
            return True

    def convertList(self, data_list: list, unit: str, desired_unit: str, verbose: bool = False) -> list:

        params = {'list': data_list, 'unit': unit, 'desired_unit': desired_unit}

        address = 'ReSpecTh/API/convertList'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print("List conversion successful.")

        return json.loads(request.requests.text)

    def verifyExperiment(self, experiment, status: str, verbose=False):

        identifier = experiment if type(experiment) == int else experiment.id

        params = {'status': status, 'exp_id': identifier}

        address = 'ExperimentManager/API/verifyExperiment'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print(json.loads(request.requests.text))


    def executeCurveMatching(self, x_sim: list, y_sim: list, x_exp: list,
                             y_exp: list,
                             uncertainty: list = [],
                             verbose=False,
                             **kwargs):

        params = {'x_sim': x_sim, 'y_sim': y_sim,
                  'x_exp': x_exp, 'y_exp': y_exp,
                  'uncertainty': json.dumps(uncertainty),
                  'configuration': json.dumps(kwargs if kwargs else {})}

        address = 'CurveMatching/API/executeCurveMatching'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print('Curve Matching executed successfully.')

        response = (json.loads(request.requests.text))

        return response

    def createUpdateExecutionCurveMatching(self, execution, verbose=False):
        execution_id = execution if type(execution) == int else execution.id
        params = {'execution_id': execution_id}

        address = 'CurveMatching/API/createUpdateExecutionCurveMatching'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print('Curve Matching computed successfully.')


    def curveMatchingIsRunning(self, verbose=False):
        address = 'CurveMatching/API/curveMatchingIsRunning'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params={})

        if request.requests.status_code == 200:
            if verbose:
                print('Curve Matching computed successfully.')

        return json.loads(request.requests.text)

    def getPropertyList(self, model_name, exp_id, fields, verbose=False):

        params = {'fields': fields, 'name': model_name, 'exp_id': exp_id}

        address = 'frontend/API/getPropertyList'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print(json.loads(request.requests.text))

    def prova(self, verbose=False):

        params = {'exp_list': [409, 410],
                  'chemModel_list': []}

        # address = 'CrowdSourcing/API/getNextQuestion'

        address = 'ExperimentManager/API/prova'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print('ok')

        # with open('edoardo.zip', 'wb') as fd:
        #     for chunk in request.requests.iter_content(chunk_size=128):
        #         fd.write(chunk)

        # print(request.requests.text)
        # print(request.requests.headers)
        #
        # with open('edo.zip', 'wb') as file:
        #     # for chunk in request.requests.iter_content(chunk_size=128):
        #     #     file.write(chunk)
        #     file.write(request.requests.content)
        # print(request.requests.content)
        # print(request.requests)

        # response = json.loads((json.loads(request.requests.text)))

        # return json.loads(request.requests.text)

    def createUser(self, fields, groups, verbose=False):

        params = {'fields': fields, 'groups': groups}

        address = 'createUser'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print('ok')

        # response = json.loads((json.loads(request.requests.text)))

        return json.loads(request.requests.text)
