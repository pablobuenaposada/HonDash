import pytest
from freezegun import freeze_time

from backend.devices.odometer import Odometer


class TestOdometer:
    @pytest.mark.parametrize(
        "unit, value, expected_km, expected_miles",
        (("km", 666, 666, 413), ("miles", 666, 1071, 665)),
    )
    def test_get_mileage(self, unit, value, expected_km, expected_miles):
        """
        Checks that the odometer reads the correct mileage after initialization.
        """

        odo = Odometer(value, unit)

        assert odo.get_mileage() == {"km": expected_km, "miles": expected_miles}

    def test_save(self):
        """
        Checks that the mileage increases after been some time running to a certain speed.
        """

        with freeze_time("00:00:00"):
            # setting the starting mileage to 0
            odo = Odometer()

        assert odo.get_mileage() == {"km": 0, "miles": 0}  # we are clean

        with freeze_time("01:00:00"):
            # after an hour we will notify the odometer that we have been going to 100km/h
            # the save method should return True meaning 1 km more has been traveled
            assert odo.save(100) is True

        # after an hour we should be in 100km mileage
        assert odo.get_mileage() == {"km": 100, "miles": 62}

    def test_save_not_enough_distance_traveled(self):
        """
        The mileage while calling save method should only be returned if more than one km more is not reached
        """

        with freeze_time("00:00:00"):
            # setting the starting mileage
            odo = Odometer()

        assert odo.get_mileage() == {"km": 0, "miles": 0}  # we are clean

        with freeze_time("00:00:30"):
            # after 30 secs we will notify the odometer that we have been going to 100km/h
            # since at that speed is not enough to travel a single km it´s expected to return False
            assert odo.save(100) is False

        # the mileage will remain the same
        assert odo.get_mileage() == {"km": 0, "miles": 0}
