from SciExpeM_API.Utility.RequestAPI import HTTP_TYPE, RequestAPI
import json


class _OpenSmoke(object):
    def startSimulation(self, experiment, chemModel, verbose=False):
        experiment_id = experiment if type(experiment) == int else experiment.id
        chemModel_id = chemModel if type(chemModel) == int else chemModel.id

        params = {'experiment': experiment_id, 'chemModel': chemModel_id}

        address = 'OpenSmoke/API/startSimulation'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print(json.loads(request.requests.text))
        else:
            return False

    def createFolderSimulation(self, experiment, chemModel, verbose=False):
        experiment_id = experiment if type(experiment) == int else experiment.id
        chemModel_id = chemModel if type(chemModel) == int else chemModel.id

        params = {'experiment': experiment_id, 'chemModel': chemModel_id}

        address = 'OpenSmoke/API/createFolderSimulation'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print(json.loads(request.requests.text))
        else:
            return False


    def initializeSimulation(self, experiment, chemModel, verbose=False):
        experiment_id = experiment if type(experiment) == int else experiment.id
        chemModel_id = chemModel if type(chemModel) == int else chemModel.id

        params = {'experiment': experiment_id, 'chemModel': chemModel_id}

        address = 'OpenSmoke/API/initializeSimulation'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print(request.requests.text)
            return True
        else:
            return False

    def restartExecution(self, execution, verbose=False):
        execution_id = execution if type(execution) == int else execution.id

        params = {'execution_id': execution_id}

        address = 'OpenSmoke/API/restartExecution'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.requests.status_code == 200:
            if verbose:
                print(request.requests.text)
            return True
        else:
            return False
