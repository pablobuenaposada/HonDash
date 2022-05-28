import json
import os
from unittest import mock

import pytest

from backend.devices.setup_updater import SetupUpdater
from backend.devices.setup_validator.setup_validator import SetupValidator


@pytest.fixture
def fixtures_dir():
    return os.path.join(os.path.dirname(__file__), "fixtures")


class TestSetupUpdater:
    def test_update_2_3_2(self):
        with mock.patch(
            "backend.devices.setup_updater.SetupUpdater._update_to_2_4_0",
            return_value={"version": "2.4.0"},
        ) as m__update_to_2_4_0, mock.patch(
            "backend.devices.setup_updater.SetupUpdater._update_to_2_5_0"
        ) as m__update_to_2_5_0:
            SetupUpdater().update({"version": "2.3.2"})
        assert m__update_to_2_4_0.called is True
        assert m__update_to_2_5_0.called is True

    def test_update_2_4_0(self):
        with mock.patch(
            "backend.devices.setup_updater.SetupUpdater._update_to_2_5_0"
        ) as m__update_to_2_5_0:
            SetupUpdater().update({"version": "2.4.0"})
        assert m__update_to_2_5_0.called is True

    def test_update_2_5_0(self):
        with mock.patch(
            "backend.devices.setup_updater.SetupUpdater._update_to_2_6_0"
        ) as m__update_to_2_6_0:
            SetupUpdater().update({"version": "2.5.0"})
        assert m__update_to_2_6_0.called is True

    def test_update_2_6_0(self):
        with mock.patch(
            "backend.devices.setup_updater.SetupUpdater._update_to_3_0_0"
        ) as m__update_to_3_0_0:
            SetupUpdater().update({"version": "2.6.0"})
        assert m__update_to_3_0_0.called is True

    def test_update_3_0_0(self):
        with mock.patch(
            "backend.devices.setup_updater.SetupUpdater._update_to_3_1_0"
        ) as m__update_to_3_1_0:
            SetupUpdater().update({"version": "3.0.0"})
        assert m__update_to_3_1_0.called is True

    def test_update_3_1_0(self):
        with mock.patch(
            "backend.devices.setup_updater.SetupUpdater._update_to_3_2_0"
        ) as m__update_to_3_2_0:
            SetupUpdater().update({"version": "3.1.0"})
        assert m__update_to_3_2_0.called is True

    def test_update_3_2_0(self):
        with mock.patch(
            "backend.devices.setup_updater.SetupUpdater._update_to_3_3_0"
        ) as m__update_to_3_3_0:
            SetupUpdater().update({"version": "3.2.0"})
        assert m__update_to_3_3_0.called is True

    def test_update_3_3_0(self):
        with mock.patch(
            "backend.devices.setup_updater.SetupUpdater._update_to_3_4_0"
        ) as m__update_to_3_4_0:
            SetupUpdater().update({"version": "3.3.0"})
        assert m__update_to_3_4_0.called is True

    def test_update_3_4_0(self):
        with mock.patch(
            "backend.devices.setup_updater.SetupUpdater._update_to_3_5_0"
        ) as m__update_to_3_5_0:
            SetupUpdater().update({"version": "3.4.0"})
        assert m__update_to_3_5_0.called is True

    def test_update_3_5_0(self):
        assert SetupUpdater().update({"version": "3.5.0"}) == {"version": "3.5.0"}

    def test__update_to_2_4_0(self, fixtures_dir):
        with open(os.path.join(fixtures_dir, "default_setup_2_3_2.json")) as file:
            setup = json.load(file)
        setup = SetupUpdater._update_to_2_4_0(setup)
        with open(os.path.join(fixtures_dir, "default_setup_2_4_0.json")) as file:
            fixture_2_4_0 = json.load(file)
        assert setup == fixture_2_4_0

    def test__update_to_2_5_0(self, fixtures_dir):
        with open(os.path.join(fixtures_dir, "default_setup_2_4_0.json")) as file:
            setup = json.load(file)
        setup = SetupUpdater._update_to_2_5_0(setup)
        with open(os.path.join(fixtures_dir, "default_setup_2_5_0.json")) as file:
            fixture_2_5_0 = json.load(file)
        assert setup == fixture_2_5_0

    def test__update_to_2_6_0(self, fixtures_dir):
        with open(os.path.join(fixtures_dir, "default_setup_2_5_0.json")) as file:
            setup = json.load(file)
        setup = SetupUpdater._update_to_2_6_0(setup)
        with open(os.path.join(fixtures_dir, "default_setup_2_6_0.json")) as file:
            fixture_2_6_0 = json.load(file)
        assert setup == fixture_2_6_0

    def test__update_to_3_0_0(self, fixtures_dir):
        with open(os.path.join(fixtures_dir, "default_setup_2_6_0.json")) as file:
            setup = json.load(file)
        setup = SetupUpdater._update_to_3_0_0(setup)
        with open(os.path.join(fixtures_dir, "default_setup_3_0_0.json")) as file:
            fixture_3_0_0 = json.load(file)
        assert setup == fixture_3_0_0

    def test__update_to_3_1_0(self, fixtures_dir):
        with open(os.path.join(fixtures_dir, "default_setup_3_0_0.json")) as file:
            setup = json.load(file)
        setup = SetupUpdater._update_to_3_1_0(setup)
        with open(os.path.join(fixtures_dir, "default_setup_3_1_0.json")) as file:
            fixture_3_1_0 = json.load(file)
        assert setup == fixture_3_1_0

    def test__update_to_3_2_0(self, fixtures_dir):
        with open(os.path.join(fixtures_dir, "default_setup_3_1_0.json")) as file:
            setup = json.load(file)
        setup = SetupUpdater._update_to_3_2_0(setup)
        with open(os.path.join(fixtures_dir, "default_setup_3_2_0.json")) as file:
            fixture_3_2_0 = json.load(file)
        assert setup == fixture_3_2_0

    def test__update_to_3_3_0(self, fixtures_dir):
        with open(os.path.join(fixtures_dir, "default_setup_3_2_0.json")) as file:
            setup = json.load(file)
        setup = SetupUpdater._update_to_3_3_0(setup)
        with open(os.path.join(fixtures_dir, "default_setup_3_3_0.json")) as file:
            fixture_3_3_0 = json.load(file)
        assert setup == fixture_3_3_0

    def test__update_to_3_4_0(self, fixtures_dir):
        with open(os.path.join(fixtures_dir, "default_setup_3_3_0.json")) as file:
            setup = json.load(file)
        setup = SetupUpdater._update_to_3_4_0(setup)
        with open(os.path.join(fixtures_dir, "default_setup_3_4_0.json")) as file:
            fixture_3_4_0 = json.load(file)
        assert setup == fixture_3_4_0

    def test__update_to_3_5_0(self, fixtures_dir):
        with open(os.path.join(fixtures_dir, "default_setup_3_4_0.json")) as file:
            setup = json.load(file)
        setup = SetupUpdater._update_to_3_5_0(setup)
        with open(os.path.join(fixtures_dir, "default_setup_3_5_0.json")) as file:
            fixture_3_5_0 = json.load(file)
        assert setup == fixture_3_5_0
        SetupValidator().validate(
            setup
        )  # this only could be applied to the last version update test
