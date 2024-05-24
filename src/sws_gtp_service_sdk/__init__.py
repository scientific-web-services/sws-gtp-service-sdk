__version__ = '0.7.1'

import json
from enum import Enum
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
        self._geophires_parameters = geophires_parameters

    def get_geophires_parameters(self) -> GeophiresParameters:
        return self._geophires_parameters


class GeophiresResult:
    def __init__(self, result: dict):
        self.geophires_result = result

    @property
    def result_id(self) -> str:
        return self.geophires_result['ResultId']


class DescribeGeophiresResultsRequest:
    def __init__(self, result_id: str = None):
        self.result_id = result_id

class DescribeGeophiresResultsResult:
    def __init__(self, geophires_results:list[GeophiresResult]):
        self.geophires_results = geophires_results

class DeleteGeophiresResultRequest:
    def __init__(self, result_id: str):
        self.result_id = result_id

class DeleteGeophiresResultResult:
    def __init__(self, result_id: str):
        self.result_id = result_id


class SharePolicy(str, Enum):
    PUBLIC = '*'
    PRIVATE = ''


class UpdateGeophiresResultRequest:
    def __init__(self, result_id: str = None, description: str = None, share_policy: SharePolicy = None):
        self.result_id = result_id
        self.description = description
        self.share_policy = share_policy


class UpdateGeophiresResultResult:
    def __init__(self, result_id: str):
        self.result_id = result_id


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
    def __init__(self, endpoint: str, api_key: str = None, auth_token:str = None):
        self._endpoint = endpoint
        self._session = requests.Session()

        # x-api-key
        self._api_key = api_key

        self._auth_token = auth_token

        retries = Retry(total=3,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])

        self._session.mount('https://', HTTPAdapter(max_retries=retries))

        # TODO should probably enable closing session

    def get_geophires_result(self, geophires_request: GeophiresRequest) -> GeophiresResult:

        response = self._session.post(
            f'{self._endpoint}/get-geophires-result',
            json={
                'geophires_input_parameters': geophires_request.get_geophires_parameters().get_parameters()},
            timeout=30,
            headers=self._get_api_key_headers()
        )
        response_dict:dict = json.loads(response.text)

        if 'message' in response_dict and response_dict['message'] == 'Endpoint request timed out':
            raise requests.Timeout(response_dict['message'])

        return GeophiresResult(response_dict)

    def get_hip_ra_result(self, hip_ra_request: HipRaRequest):
        response = self._session.post(
            f'{self._endpoint}/get-hip-ra-result',
            json={
                'hip_ra_input_parameters': hip_ra_request.get_hip_ra_parameters().get_parameters()},
            timeout=30,
            headers=self._get_api_key_headers()
        )
        return HipRaResult(json.loads(response.text))

    def create_geophires_result(self, geophires_request: GeophiresRequest) -> GeophiresResult:
        response = self._session.post(
            f'{self._endpoint}/create-geophires-result',
            json={
                'geophires_input_parameters': geophires_request.get_geophires_parameters().get_parameters()},
            timeout=30,
            headers=self._get_auth_token_headers()
        )
        response_dict: dict = json.loads(response.text)

        if 'message' in response_dict and response_dict['message'] == 'Endpoint request timed out':
            raise requests.Timeout(response_dict['message'])

        return GeophiresResult(response_dict)

    def describe_geophires_results(self,
                                   request: DescribeGeophiresResultsRequest = None) -> DescribeGeophiresResultsResult:
        filters = {}
        if request is not None and request.result_id is not None:
            filters['result_id'] = request.result_id

        response = self._session.post(
            f'{self._endpoint}/describe-geophires-results',
            timeout=30,
            json=filters,
            headers=self._get_auth_token_headers()
        )
        response_list: list[dict[str,Any]] = json.loads(response.text)

        if 'message' in response_list and response_list['message'] == 'Endpoint request timed out':
            raise requests.Timeout(response_list['message'])

        return DescribeGeophiresResultsResult([GeophiresResult(entry) for entry in response_list])

    def get_shared_geophires_result(self, result_id) -> GeophiresResult:
        response = self._session.post(
            f'{self._endpoint}/get-shared-geophires-result',
            timeout=30,
            json={'result_id': result_id},
            headers=self._get_api_key_headers()
        )
        response_dict: dict = json.loads(response.text)

        if 'message' in response_dict and response_dict['message'] == 'Endpoint request timed out':
            raise requests.Timeout(response_dict['message'])

        return GeophiresResult(response_dict)

    def update_geophires_result(self, request: UpdateGeophiresResultRequest) -> UpdateGeophiresResultResult:
        update_json = {
            'result_id': request.result_id,
        }

        if request.description is not None:
            update_json['description'] = request.description

        if request.share_policy is not None:
            update_json['share_policy'] = request.share_policy.value

        response = self._session.post(
            f'{self._endpoint}/update-geophires-result',
            json=update_json,
            timeout=30,
            headers=self._get_auth_token_headers()
        )
        response_dict: dict = json.loads(response.text)

        return UpdateGeophiresResultResult(response_dict['ResultId'])


    def delete_geophires_result(self, request:DeleteGeophiresResultRequest) -> DeleteGeophiresResultResult:
        response = self._session.post(
            f'{self._endpoint}/delete-geophires-result',
            json={
                'result_id': request.result_id
            },
            timeout=30,
            headers=self._get_auth_token_headers()
        )
        response_dict: dict = json.loads(response.text)

        return DeleteGeophiresResultResult(response_dict['ResultId'])

    def _get_api_key_headers(self):
        headers = {}
        if self._api_key is not None:
            headers['x-api-key'] = self._api_key

        return headers

    def _get_auth_token_headers(self):
        headers = {}
        if self._auth_token is not None:
            headers['Authorization'] = f'Bearer {self._auth_token}'

        return headers
