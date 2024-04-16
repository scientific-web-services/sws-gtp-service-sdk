__version__ = '0.3.0'

import json
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from requests.adapters import Retry


class GeophiresSimulationParameters:
    def __init__(self):
        self._parameters = {}

    def get_parameters(self) -> dict:
        return self._parameters

    def with_gradient_1(self, gradient_1: float):  # -> Self:
        return self.with_parameter('Gradient 1', gradient_1)

    def with_maximum_temperature(self, max_temp: float):  # -> Self:
        return self.with_parameter('Maximum Temperature', max_temp)

    def with_reservoir_model(self, reservoir_model: int):  # -> Self:
        return self.with_parameter('Reservoir Model', reservoir_model)

    def with_parameter(self, parameter_name: str, parameter_value: Any):  # -> Self:
        self._parameters[parameter_name] = parameter_value
        return self


class GeophiresSimulationRequest:
    def __init__(self, simulation_parameters: GeophiresSimulationParameters):
        self._simulation_parameters = simulation_parameters

    def get_simulation_parameters(self) -> GeophiresSimulationParameters:
        return self._simulation_parameters


class GeophiresSimulationResult:
    def __init__(self, simulation_result: dict):
        self.simulation_result = simulation_result


class GeophiresServiceClient:
    def __init__(self, endpoint: str, api_key:str = None):
        self._endpoint = endpoint
        self._session = requests.Session()

        # x-api-key
        self._api_key = api_key

        retries = Retry(total=3,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])

        self._session.mount('https://', HTTPAdapter(max_retries=retries))

        # TODO should probably enable closing session

    def get_geophires_simulation_result(self, geophires_simulation_request: GeophiresSimulationRequest):
        # -> GeophiresSimulationResult:

        response = self._session.post(
            self._endpoint,
            json={
                'geophires_input_parameters': geophires_simulation_request.get_simulation_parameters().get_parameters()},
            timeout=30,
            headers={'x-api-key': self._api_key} if self._api_key is not None else None
        )
        return GeophiresSimulationResult(json.loads(response.text))
