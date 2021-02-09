import requests
from requests.exceptions import RequestException
from .settings import IP, PORT, TOKEN, HTTPS
from enum import Enum
from django.db.models import Q
from .QSerializer import QSerializer
from .Models import *
import json
import sys
from .exceptionsAPI import *
import os

from datetime import datetime


def check_status_code(request):
    status_code = int(request.requests.status_code)
    if status_code >= 500:
        raise HTTP_SERVER_EXCEPTION(status_code)
    elif 400 <= status_code <= 499:
        raise HTTP_CLIENT_EXCEPTION(status_code)
    elif 300 <= status_code <= 399:
        raise HTTP_REDIRECTION_EXCEPTION(status_code)
    elif status_code <= 299:
        response = json.loads(request.text)
        if response['error']:
            raise API_PROCESSING_EXCEPTION(response['error'])
        else:
            return response


class HTTP_TYPE(Enum):
    GET = 0
    POST = 1


class RequestAPI:
    def __init__(self, ip: str, port: int, address: str, params: dict, token: str, mode: HTTP_TYPE):
        self.ip = ip
        self.port = port
        self.params = params
        self.token = token
        self.mode = mode
        self.headers = {"Authorization": "Token " + token}
        if HTTPS:
            init = "https://"
        else:
            init = "http://"
        url = init + ip + ":" + str(port) + "/" + address

        if mode == HTTP_TYPE.GET:
            self.requests = requests.get(url, headers=self.headers, params=self.params)
        elif mode == HTTP_TYPE.POST:
            self.requests = requests.post(url, headers=self.headers, data=self.params)

        self.transfer_attribute()

    def transfer_attribute(self):
        list_attribute = [x for x in dir(self.requests) if "__" not in x]
        for attribute in list_attribute:
            setattr(self, attribute, getattr(self.requests, attribute))


def getUserInfo(username, password):
    if HTTPS:
        init = "https://"
    else:
        init = "http://"

    address = "getInfoUser"

    params = {'username': username, 'password': password}

    url = init + IP + ":" + str(PORT) + "/" + address

    request = requests.post(url, data=params)

    status_code = int(request.status_code)
    if status_code >= 500:
        raise HTTP_SERVER_EXCEPTION(status_code)
    elif 400 <= status_code <= 499:
        raise HTTP_CLIENT_EXCEPTION(status_code)
    elif 300 <= status_code <= 399:
        raise HTTP_REDIRECTION_EXCEPTION(status_code)
    elif status_code <= 299:
        response = json.loads(request.text)
        # token = response.get('token')
        # username = response.get('username')
        # user_id = response.get('user_id')
        # first_name = response.get('first_name')
        # last_name = response.get('last_name')
        # email = response.get('email')
        # groups = response.get('groups')
        # permissions = response.get('permissions')
        return response



# START FILTER


def schemaFilter(address, model, *args, **kwargs):
    q_serializer = QSerializer()
    result = []
    try:
        request = RequestAPI(ip=IP,
                             port=PORT,
                             params={"query": q_serializer.dumps(Q(*args, **kwargs))},
                             address=address,
                             token=TOKEN,
                             mode=HTTP_TYPE.GET)

        response = check_status_code(request)

        if response['result']:
            for r in response['result']:
                element = model.from_dict(r)
                result.append(element)

        return result

    except (RequestException, ConnectionRefusedError, ConnectionError):
        raise API_CONNECTION_EXCEPTION


def filterExperiment(*args, **kwargs):
    return schemaFilter("ExperimentManager/API/filterExperiment",
                        Experiment,
                        *args,
                        **kwargs)


def filterChemModel(*args, **kwargs):
    return schemaFilter("ExperimentManager/API/filterChemModel",
                        ChemModel,
                        *args,
                        **kwargs)


def filterExecution(*args, **kwargs):
    return schemaFilter("ExperimentManager/API/filterExecution",
                        Execution,
                        *args,
                        **kwargs)


def filterCurveMatchingResult(*args, **kwargs):
    return schemaFilter("ExperimentManager/API/filterCurveMatchingResult",
                        CurveMatchingResult,
                        *args,
                        **kwargs)


# END FILTER


# START INSERT

def default_serializer(obj, mapping):
    if not mapping or obj.__class__ not in mapping:
        return obj.serialize()
    exclude_fields = mapping[obj.__class__]
    return obj.serialize(exclude_fields)


def schemaInsert(address, obj, mapping=None, verbose=False):
    if mapping is None:
        mapping = {}
    object_serialized = json.dumps(obj, default=lambda o: default_serializer(o, mapping))

    dimension = round(sys.getsizeof(object_serialized) / 1000.0, 3)
    if verbose:
        print("Send Insert Request %s %f KB" % (obj.__class__.__name__, dimension))

    try:
        request = RequestAPI(ip=IP,
                             port=PORT,
                             params={"object": object_serialized},
                             address=address,
                             token=TOKEN,
                             mode=HTTP_TYPE.POST)

        response = check_status_code(request)

        if response['result']:
            if response['result'] == "OK":
                if verbose:
                    print("Insert Succeeded!")
            elif response['result'] == "DUPLICATE":
                if verbose:
                    print("Insert Failed! Duplicate Element")

    except (RequestException, ConnectionRefusedError, ConnectionError):
        raise API_CONNECTION_EXCEPTION


def insertChemModel(chemModel, verbose=False):
    return schemaInsert(address="ExperimentManager/API/insertChemModel", obj=chemModel, verbose=verbose)


def insertExperiment(experiment, verbose=False):
    return schemaInsert(address="ExperimentManager/API/insertExperiment", obj=experiment, verbose=verbose)


def insertExecution(execution, verbose=False):
    return schemaInsert(address="ExperimentManager/API/insertExecution",
                        obj=execution,
                        mapping={
                            ChemModel: ['xml_file_kinetics', 'xml_file_reaction_names', 'version'],
                            Experiment: ['reactor', 'experiment_type', 'FilePaper', 'ignition_type', 'xml_file',
                                         'os_input_file', 'DataColumn', 'InitialSpecie', 'CommonProperty']},
                        verbose=verbose)


def loadXMLExperiment(path, verbose=False):
    if not os.path.isfile(path):
        raise FileNotFoundError(path)

    object_serialized = json.dumps({"file": open(path, 'r').read()})

    dimension = round(sys.getsizeof(object_serialized) / 1000.0, 3)
    if verbose:
        print("Send Insert Request Experiment XML %f KB" % dimension)

    try:
        request = RequestAPI(ip=IP,
                             port=PORT,
                             params={"query": object_serialized},
                             address="ExperimentManager/API/loadXMLExperiment",
                             token=TOKEN,
                             mode=HTTP_TYPE.POST)

        response = check_status_code(request)

        if response['result']:
            if response['result'] == "OK":
                if verbose:
                    print("Insert Succeeded!")
            elif response['result'] == "DUPLICATE":
                if verbose:
                    print("Insert Failed! Duplicate Element")

    except (RequestException, ConnectionRefusedError, ConnectionError):
        raise API_CONNECTION_EXCEPTION

# -->No sense of this function
# def insertCurveMatchingResult(curveMatchingResult, verbose=False):
#     return schemaInsert(address="ExperimentManager/API/insertCurveMatchingResult",
#                         obj=curveMatchingResult,
#                         mapping={
#                             ExecutionColumn: ['name', 'label', 'units', 'species', 'execution',
#                                               'data', 'file_type']},
#                         verbose=verbose)

# END INSERT


# START EXECUTE

def schemaExecuteBase(address, **kwargs):
    try:
        request = RequestAPI(ip=IP,
                             port=PORT,
                             params={"query": json.dumps(kwargs)},
                             address=address,
                             token=TOKEN,
                             mode=HTTP_TYPE.POST)

        response = check_status_code(request)

        if response['result']:
            return response['result']

        return ()

    except (RequestException, ConnectionRefusedError, ConnectionError):
        raise API_CONNECTION_EXCEPTION


def executeOptimaPP(**kwargs):
    return schemaExecuteBase("ReSpecTh/API/executeOptimaPP", **kwargs)


# Don't use it is a locking request TODO make it async
def executeCurveMatchingBase(**kwargs):
    result = schemaExecuteBase("CurveMatching/API/executeCurveMatchingBase", **kwargs)
    return result

# END EXECUTE


def basic_request(address, params, verbose):
    try:
        request = RequestAPI(ip=IP,
                             port=PORT,
                             params={"params": json.dumps(params)},
                             address=address,
                             token=TOKEN,
                             mode=HTTP_TYPE.POST)

        # response = check_status_code(request)

        if verbose:
            print(request.requests.status_code, request.requests.text)

    except (RequestException, ConnectionRefusedError, ConnectionError):
        raise API_CONNECTION_EXCEPTION

# START SIMULATION


def startSimulation(experiment, chemModel, verbose=False):
    exp_id = experiment.id
    chemModel_id = chemModel.id
    address = "OpenSmoke/API/startSimulation"
    params = {'experiment': exp_id, 'chemModel': chemModel_id}
    basic_request(address, params, verbose)



# END SIMULATION

# START Verify Experiment


def verifyExperiment(experiment, status, verbose=False):
    exp_id = experiment.id

    address = "ExperimentManager/API/verifyExperiment/"

    params = {'experiment': exp_id, 'status': status}

    basic_request(address, params, verbose)

# END Verify Experiment


# START UPDATE

def insertOSFile(experiment, osFile, verbose=False):
    exp_id = experiment.id

    address = "ExperimentManager/API/insertOSFileAPI/"

    params = {'experiment': exp_id, 'osFile': osFile}

    basic_request(address, params, verbose)

# END UPDATE


# START ANALYZE

def analyzeExecution(execution, verbose=False):
    exec_id = execution.id

    address = "ExperimentManager/API/analyzeExecution/"

    params = {'execution': exec_id}

    basic_request(address, params, verbose)

# END ANALYZE


def prova(verbose=True):
    # exp_id = experiment.id

    address = "CurveMatching/API/executeCurveMatchingBase"

    # params = {'execution': 1, 'file': open("ParametricAnalysisIDT.out").read(), 'file_type': 'IDT'}
    params ={}
    basic_request(address, params, verbose)