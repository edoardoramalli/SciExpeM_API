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

    def filter(self, model_name: str, verbose=False, query=None, *args, **kwargs) -> list:
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




