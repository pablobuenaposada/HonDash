from concurrent.futures import TimeoutError
from unittest import mock

import pytest

from backend.devices.gps import Gps


class TestGps:
    @pytest.mark.parametrize("exception", (TimeoutError, ConnectionRefusedError))
    def test_connection_error(self, exception):
        """Checks that if gpsd connection timeouts or no gps is connected it doesn't block the thread execution"""
        with mock.patch("backend.devices.gps.gpsd.connect") as m_connect:
            m_connect.side_effect = exception
            gps = Gps()
        assert gps.status is False
        assert gps.speed == 0
