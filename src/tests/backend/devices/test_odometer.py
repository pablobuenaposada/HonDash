from unittest.mock import patch

import pytest
from freezegun import freeze_time

from backend.devices.odometer import Odometer
from backend.devices.setup_file import DEFAULT_CONFIG_FILE_NAME


@patch("backend.devices.setup_file.FILE_NAME", DEFAULT_CONFIG_FILE_NAME)
class TestOdometer:
    @pytest.mark.parametrize(
        "unit, value, expected_km, expected_miles",
        (("km", 666, 666, 413), ("miles", 666, 1071, 665)),
    )
    def test_get_mileage(self, unit, value, expected_km, expected_miles):
        """
        Checks that the odometer reads the correct mileage after setting the value in the json setup file.
        """

        with patch("backend.devices.odometer.SetupFile.get_value") as m_get_value:
            m_get_value.return_value = {"value": value, "unit": unit}
            odo = Odometer()

        assert odo.get_mileage() == {"km": expected_km, "miles": expected_miles}

    def test_get_mileage_no_mileage_found(self):
        """
        If no mileage is found in the setup file, the odometer should start from 0
        """

        with patch("backend.devices.odometer.SetupFile.get_value") as m_get_value:
            m_get_value.side_effect = AttributeError
            odo = Odometer()

        assert odo.get_mileage() == {"km": 0, "miles": 0}

    def test_save(self):
        """
        Checks that the mileage increases after been some time running to a certain speed.
        """

        with freeze_time("00:00:00"):
            # setting the starting mileage
            with patch("backend.devices.odometer.SetupFile.get_value") as get_value:
                get_value.return_value = {"value": 0}
                odo = Odometer()

        assert odo.get_mileage() == {"km": 0, "miles": 0}  # we are clean

        with freeze_time("01:00:00"):
            # after an hour we will notify the odometer that we have been going to 100km/h
            with patch("backend.devices.odometer.SetupFile.update_key") as m_update_key:
                odo.save(100)
                # checking that we tried to save the new mileage into the setup file
                m_update_key.assert_called_with("odo", {"value": 100})

        # after an hour we should be in 100km mileage
        assert odo.get_mileage() == {"km": 100, "miles": 62}

    def test_save_not_enough_distance_traveled(self):
        """
        The mileage should not increase if more than one km more is not reached
        """

        with freeze_time("00:00:00"):
            # setting the starting mileage
            with patch("backend.devices.odometer.SetupFile.get_value") as get_value:
                get_value.return_value = {"value": 0}
                odo = Odometer()

        assert odo.get_mileage() == {"km": 0, "miles": 0}  # we are clean

        with freeze_time("00:00:30"):
            # after 30 secs we will notify the odometer that we have been going to 100km/h
            with patch("backend.devices.odometer.SetupFile.update_key") as m_update_key:
                odo.save(100)
                # checking that we couldn't reach one km more so no update to the setup file is needed
                m_update_key.assert_not_called()

        # the mileage will remain the same
        assert odo.get_mileage() == {"km": 0, "miles": 0}
