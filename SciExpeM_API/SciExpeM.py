import requests
from enum import Enum
from .QSerializer import QSerializer
from django.db.models import Q
import json
# from Models import *
# import SciExpeM_API.Models as Models
from .Utility.RequestAPI import HTTP_TYPE, RequestAPI
from .Utility.Tools import optimize
from SciExpeM_API import settings

import os


class SciExpeM:

    def __init__(self, ip, port, token, secure):
        self.ip = ip
        self.port = port
        self.token = token
        self.secure = secure

        settings.IP = self.ip
        settings.PORT = self.port
        settings.TOKEN = self.token
        settings.SECURE = self.secure
        settings.DB = self

        self.Experiment = {}
        self.ChemModel = {}
        self.CommonProperty = {}
        self.CurveMatchingResult = {}
        self.DataColumn = {}
        self.Execution = {}
        self.ExecutionColumn = {}
        self.FilePaper = {}
        self.InitialSpecie = {}

    def filterDatabase(self, model_name: str, verbose=False, query=None, *args, **kwargs) -> list:
        q_serializer = QSerializer()

        q = q_serializer.dumps(query) if query else q_serializer.dumps(Q(*args, **kwargs))

        params = {'model': model_name, 'query': q}

        address = 'ExperimentManager/API/filterDataBase'

        request = RequestAPI(ip=self.ip,
                             port=self.port,
                             address=address,
                             token=self.token,
                             mode=HTTP_TYPE.POST,
                             secure=self.secure,
                             params=params)

        if request.requests.status_code != 200:
            return []
        else:
            if verbose:
                print("Filter Request Successful.")
            return optimize(self, model_name, request.requests.text)

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
                print(request.requests.text)

    def updateElement(self, model_name: str, element, verbose=False, **kwargs):

        identifier = element if type(element) == int else element.id

        params = {'model_name': model_name, 'property': json.dumps(kwargs), 'id': identifier}

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
                print("Update Element Parameter Successful.")

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




