from SciExpeM_API.Utility.RequestAPI import HTTP_TYPE, RequestAPI

import json
import os


class _ReSpecTh(object):
    def executeOptimaPP(self, text: str, verbose=False) -> str:
        params = {'text': text}

        address = 'ReSpecTh/API/executeOptimaPP'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.status_code != 200:
            return ''
        else:
            if verbose:
                print("XML ReSpecTh created successfully.")
            return json.loads(request.requests.text)

    def executeOptimaPPExperiment(self, experiment, verbose=False) -> str:
        experiment_id = experiment if type(experiment) == int else experiment.id

        params = {'exp_id': experiment_id}

        address = 'ReSpecTh/API/executeOptimaPPExperiment'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.status_code != 200:
            return ''
        else:
            if verbose:
                print("XML ReSpecTh created successfully.")
            return json.loads(request.requests.text)


    def createTxtOptimaPP(self, experiment, verbose=False) -> str:
        experiment_id = experiment if type(experiment) == int else experiment.id

        params = {'exp_id': experiment_id}

        address = 'ReSpecTh/API/createTxtOptimaPP'

        request = RequestAPI(address=address, mode=HTTP_TYPE.POST, params=params)

        if request.status_code != 200:
            return ''
        else:
            if verbose:
                print("Txt OptimaPP created successfully.")
            return json.loads(request.requests.text)

