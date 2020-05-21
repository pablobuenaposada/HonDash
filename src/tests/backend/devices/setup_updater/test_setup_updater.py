import json
import os
from unittest import mock

import pytest

from backend.devices.setup_updater import SetupUpdater


@pytest.fixture
def fixtures_dir():
    return os.path.join(os.path.dirname(__file__), "fixtures")


class TestSetupUpdater:
    def test_update_2_4_0(self):
        assert SetupUpdater().update({"version": "2.4.0"}) == {"version": "2.4.0"}

    def test_update_2_3_2(self):
        with mock.patch(
            "backend.devices.setup_updater.SetupUpdater._update_to_2_4_0"
        ) as m__update_to_2_4_0:
            SetupUpdater().update({"version": "2.3.2"})
        assert m__update_to_2_4_0.called is True

    def test__update_to_2_4_0(self, fixtures_dir):
        with open(os.path.join(fixtures_dir, "default_setup_2_3_2.json")) as file:
            setup = json.load(file)
        setup = SetupUpdater._update_to_2_4_0(setup)
        with open(os.path.join(fixtures_dir, "default_setup_2_4_0.json")) as file:
            fixture_2_4_0 = json.load(file)
        assert setup == fixture_2_4_0
