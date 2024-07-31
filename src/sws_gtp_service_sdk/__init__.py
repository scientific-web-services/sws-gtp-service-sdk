__version__ = '0.8.0'

import json
import os
from enum import Enum
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from requests.adapters import Retry
from warrant import AWSSRP


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
        self._geophires_parameters = geophires_parameters

    def get_geophires_parameters(self) -> GeophiresParameters:
        return self._geophires_parameters


class GeophiresResult:
    def __init__(self, result: dict):
        self.geophires_result = result

    @property
    def result_id(self) -> str:
        return self.geophires_result['ResultId']


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


class GtpCredentialHelper:
    def __init__(self):
        self.config: dict[str, str] = {
            'pool_id': 'us-west-2_HELsUMzkF',
            'client_id': '4tq6utj5ovsd3hvejbhi91nhds',
        }

    def auth_token(self) -> str:
        user_id = os.environ.get('SWS_GTP_API_ACCESS_USER_ID')
        password = os.environ.get('SWS_GTP_API_ACCESS_PASSWORD')

        aws = AWSSRP(
            username=user_id,
            pool_id=self.config['pool_id'],
            client_id=self.config['client_id'],
            password=password,
        )
        tokens = aws.authenticate_user()

        # id_token = str(tokens['AuthenticationResult']['IdToken'])
        # refresh_token = tokens['AuthenticationResult']['RefreshToken']
        access_token = tokens['AuthenticationResult']['AccessToken']
        # token_type = tokens['AuthenticationResult']['TokenType']

        return str(access_token)


class GtpServiceClient:
    def __init__(self, endpoint: str = 'https://api.gtp.scientificweb.services', auth_token: str | None = None):
        self._endpoint = endpoint
        self._session = requests.Session()

        self._auth_token = auth_token if auth_token is not None else GtpCredentialHelper().auth_token()

        retries = Retry(total=3,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])

        self._session.mount('https://', HTTPAdapter(max_retries=retries))

        # TODO should probably enable closing session

    def get_geophires_result(self, geophires_request: GeophiresRequest) -> GeophiresResult:

        response = self._session.post(
            f'{self._endpoint}/v1/get-geophires-result',
            json={
                'geophires_input_parameters': geophires_request.get_geophires_parameters().get_parameters()},
            timeout=30,
            headers=self._get_auth_token_headers()
        )
        response_dict: dict = self._get_response_dict(response)

        return GeophiresResult(response_dict)

    def get_hip_ra_result(self, hip_ra_request: HipRaRequest):
        response = self._session.post(
            f'{self._endpoint}/v1/get-hip-ra-result',
            json={
                'hip_ra_input_parameters': hip_ra_request.get_hip_ra_parameters().get_parameters()},
            timeout=30,
            headers=self._get_auth_token_headers()
        )
        return HipRaResult(self._get_response_dict(response))

    def _get_auth_token_headers(self):
        headers = {}
        if self._auth_token is not None:
            headers['Authorization'] = f'Bearer {self._auth_token}'

        return headers

    def _get_response_list(self, response: requests.Response) -> list[dict[str, Any]]:
        response_obj = json.loads(response.text)
        self._raise_exception_if_error_response(response_obj)

        return response_obj

    def _get_response_dict(self, response: requests.Response) -> dict[str, Any]:
        response_dict = json.loads(response.text)
        self._raise_exception_if_error_response(response_dict)

        if 'message' in response_dict and response_dict['message'] == 'Endpoint request timed out':
            raise requests.Timeout(response_dict['message'])

        return response_dict

    def _raise_exception_if_error_response(self, response_obj: Any) -> None:
        if isinstance(response_obj, dict):
            response_dict: dict[str, Any] = response_obj
            if 'message' in response_dict and response_dict['message'] == 'Endpoint request timed out':
                raise requests.Timeout(response_obj['message'])

            if 'error' in response_dict:
                # TODO custom exceptions
                raise RuntimeError(response_dict['error'])
