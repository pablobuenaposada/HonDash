import datetime

from freezegun import freeze_time

from devices.style import AVAILABLE_STATUSES, Style


class TestStyle:
    def test_initial_status(self):
        """
        Initial status is day mode
        """
        style = Style()
        assert style.status == AVAILABLE_STATUSES[0]

    def test_update_change_status(self):
        """
        Status should change if the tps is within the range for specific amount of time
        """
        style = Style()
        tps_within_range = (
            style.threshold_lower_limit
        )  # the lower limit is inside the range
        seconds_to_switch_status = style.elapsed_seconds
        start_time = datetime.datetime.now()

        # starting in day mode
        with freeze_time(start_time):
            style.update(tps_within_range)
            assert style.status == AVAILABLE_STATUSES[0]

        # not reaching the seconds needed to switch status
        with freeze_time(
            start_time + datetime.timedelta(0, seconds_to_switch_status - 1)
        ):
            style.update(tps_within_range)
            assert style.status == AVAILABLE_STATUSES[0]

        # reaching the seconds needed to switch status
        with freeze_time(start_time + datetime.timedelta(0, seconds_to_switch_status)):
            style.update(tps_within_range)
            assert style.status == AVAILABLE_STATUSES[1]

    def test_update_no_change_status(self):
        """
        Status should not change if the tps is not within the range
        """
        style = Style()
        tps_outside_range = (
            style.threshold_upper_limit + 1
        )  # the upper limit + 1 is outside the range
        seconds_to_switch_status = style.elapsed_seconds
        start_time = datetime.datetime.now()

        # starting in day mode
        with freeze_time(start_time):
            style.update(tps_outside_range)
            assert style.status == AVAILABLE_STATUSES[0]

        # not reaching the seconds needed to switch status
        with freeze_time(
            start_time + datetime.timedelta(0, seconds_to_switch_status - 1)
        ):
            style.update(tps_outside_range)
            assert style.status == AVAILABLE_STATUSES[0]

        # reaching the seconds needed to switch status but,
        # in this case we never been in the tps range so no status change should be performed.
        with freeze_time(start_time + datetime.timedelta(0, seconds_to_switch_status)):
            style.update(tps_outside_range)
            assert style.status == AVAILABLE_STATUSES[0]

    def test_from_night_to_day(self):
        """
        We should be also allowed to go back from night mode to day
        """
        style = Style()
        tps_within_range = (
            style.threshold_lower_limit
        )  # the lower limit is inside the range
        seconds_to_switch_status = style.elapsed_seconds
        start_time = datetime.datetime.now()

        with freeze_time(start_time):
            style.update(tps_within_range)

        # night mode
        with freeze_time(start_time + datetime.timedelta(0, seconds_to_switch_status)):
            style.update(tps_within_range)
            assert style.status == AVAILABLE_STATUSES[1]

        style.update(tps_within_range)

        # coming back to day mode
        with freeze_time(
            start_time + datetime.timedelta(0, seconds_to_switch_status * 2)
        ):
            style.update(tps_within_range)
            assert style.status == AVAILABLE_STATUSES[0]
