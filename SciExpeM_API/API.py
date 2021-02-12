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


# START ANALYZE

def analyzeExecution(execution, verbose=False):
    exec_id = execution.id

    address = "ExperimentManager/API/analyzeExecution/"

    params = {'execution': exec_id}

    basic_request(address, params, verbose)

# END ANALYZE
