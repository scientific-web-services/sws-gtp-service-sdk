__version__ = '0.5.0'

import json
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from requests.adapters import Retry



class GeophiresParameters:
    def __init__(self):
        self._parameters = {}

    def get_parameters(self) -> dict:
        return self._parameters


    def with_parameter(self, parameter_name: str, parameter_value: Any):  # -> Self:
        self._parameters[parameter_name] = parameter_value
        return self

    def with_gradient_1(self, gradient_1: float):  # -> Self:
        """TODO autogenerate from model"""
        return self.with_parameter('Gradient 1', gradient_1)

    def with_maximum_temperature(self, max_temp: float):  # -> Self:
        """TODO autogenerate from model"""
        return self.with_parameter('Maximum Temperature', max_temp)

    def with_reservoir_model(self, reservoir_model: int):  # -> Self:
        """TODO autogenerate from model"""
        return self.with_parameter('Reservoir Model', reservoir_model)


class GeophiresRequest:
    def __init__(self, geophires_parameters: GeophiresParameters):
        self._simulation_parameters = geophires_parameters

    def get_geophires_parameters(self) -> GeophiresParameters:
        return self._simulation_parameters


class GeophiresResult:
    def __init__(self, simulation_result: dict):
        self.simulation_result = simulation_result


class HipRaParameters:
    def __init__(self):
        self._parameters = {}

    def get_parameters(self) -> dict:
        return self._parameters

    def with_parameter(self, parameter_name: str, parameter_value: Any):  # -> Self:
        self._parameters[parameter_name] = parameter_value
        return self


class HipRaRequest:
    def __init__(self, parameters: HipRaParameters):
        self._parameters = parameters

    def get_hip_ra_parameters(self) -> HipRaParameters:
        return self._parameters


class HipRaResult:
    def __init__(self, result: dict):
        self.hip_ra_result: dict = result

class GtpServiceClient:
    def __init__(self, endpoint: str, api_key: str = None):
        self._endpoint = endpoint
        self._session = requests.Session()

        # x-api-key
        self._api_key = api_key

        retries = Retry(total=3,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])

        self._session.mount('https://', HTTPAdapter(max_retries=retries))

        # TODO should probably enable closing session

    def get_geophires_result(self, geophires_request: GeophiresRequest):
        # -> GeophiresResult:

        response = self._session.post(
            f'{self._endpoint}/get-geophires-result',
            json={
                'geophires_input_parameters': geophires_request.get_geophires_parameters().get_parameters()},
            timeout=30,
            headers={'x-api-key': self._api_key} if self._api_key is not None else None
        )
        return GeophiresResult(json.loads(response.text))

    def get_hip_ra_result(self, hip_ra_request: HipRaRequest):
        response = self._session.post(
            f'{self._endpoint}/get-hip-ra-result',
            json={
                'hip_ra_input_parameters': hip_ra_request.get_hip_ra_parameters().get_parameters()},
            timeout=30,
            headers={'x-api-key': self._api_key} if self._api_key is not None else None
        )
        return HipRaResult(json.loads(response.text))
