import unittest

from sws_gtp_service_sdk import GtpServiceClient
from sws_gtp_service_sdk import GeophiresSimulationParameters
from sws_gtp_service_sdk import GeophiresSimulationRequest


class GtpServiceSdkTest(unittest.TestCase):
    def test_get_geophires_simulation_result(self):
        client = GtpServiceClient()
        result = client.get_geophires_simulation_result(
            GeophiresSimulationRequest(
                GeophiresSimulationParameters()
                .with_gradient_1(50)
                .with_maximum_temperature(300)
                .with_reservoir_model(1)
            )
        )
        assert result is not None
