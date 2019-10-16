from unittest.mock import patch

from freezegun import freeze_time

from devices.odometer import Odometer


class TestOdometer:
    def test_get_mileage(self):
        """
        Checks that the odometer reads the correct mileage after setting the value in the json setup file.
        """

        with patch("devices.odometer.SetupFile.get_value") as m_get_value:
            m_get_value.return_value = {"value": 666}
            odo = Odometer()

        assert odo.get_mileage() == {"km": 666, "miles": 413}

    def test_save(self):
        """
        Checks that the mileage increases after been some time running to a certain speed.
        """

        with freeze_time("00:00:00"):
            # setting the starting mileage
            with patch("devices.odometer.SetupFile.get_value") as get_value:
                get_value.return_value = {"value": 0}
                odo = Odometer()

        assert odo.get_mileage() == {"km": 0, "miles": 0}  # we are clean

        with freeze_time("01:00:00"):
            # after an hour we will notify the odometer that we have been going to 100km/h
            with patch("devices.odometer.SetupFile.update_key") as m_update_key:
                odo.save(100)
                # checking that we tried to save the new mileage into the setup file
                m_update_key.assert_called_with("odo", {"value": 100})

        # after an hour we should be in 100km mileage
        assert odo.get_mileage() == {"km": 100, "miles": 62}
