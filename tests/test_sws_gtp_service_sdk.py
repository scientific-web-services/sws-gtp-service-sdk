import unittest

from sws_gtp_service_sdk import GeophiresServiceClient
from sws_gtp_service_sdk import GeophiresSimulationParameters
from sws_gtp_service_sdk import GeophiresSimulationRequest


class GeophiresServiceSdkTest(unittest.TestCase):
    def test_get_geophires_simulation_result(self):
        client = GeophiresServiceClient()
        result = client.get_geophires_simulation_result(
            GeophiresSimulationRequest(
                GeophiresSimulationParameters()
                .with_gradient_1(50)
                .with_maximum_temperature(300)
                .with_reservoir_model(1)
            )
        )
        assert result is not None
