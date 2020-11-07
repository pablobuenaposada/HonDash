import json
import os
from shutil import copyfile
from unittest import mock

import pytest

from backend.devices import setup_file
from backend.devices.setup_validator.setup_validator import SetupValidator
from backend.main import Backend


class TestMain:
    def setup_method(self):
        # prepare the setup file where the backend expects it
        copyfile(setup_file.DEFAULT_CONFIG_FILE_NAME, setup_file.FILE_NAME)

    def teardown_method(self):
        os.remove("setup.json")  # delete setup file

    def test_run_backend(self):
        with mock.patch("usb.core.find"), mock.patch(
            "threading.Thread.start"
        ), mock.patch("backend.main.Websocket.__init__") as m_ws___init__, mock.patch(
            "backend.devices.kpro.kpro.Kpro.__init__"
        ) as m___init__:
            # mocking kpro device since for tests is not available
            m___init__.return_value = None
            # mocking websocket
            m_ws___init__.return_value = None

            assert type(Backend()) == Backend

    def test_stop(self):
        """
        You should be able to run the backend twice without any problem calling stop() between them
        """
        with mock.patch("usb.core.find"):
            b = Backend()
            b.stop()
            b = Backend()
            b.stop()

    def test_setup(self):
        """
        Setup method should return in this case the default setup json loaded previously
        """
        with mock.patch("usb.core.find"):
            b = Backend()
            setup_from_backend = b.setup()
            with open(setup_file.DEFAULT_CONFIG_FILE_NAME) as file:
                default_setup = json.load(file)
            assert setup_from_backend == default_setup
            b.stop()

    def test_save(self):
        """
        Save a new setup and retrieve it
        """
        with mock.patch("usb.core.find"):
            b = Backend()
            with open(setup_file.DEFAULT_CONFIG_FILE_NAME) as file:
                default_setup = json.load(file)
            default_setup["tps"]["label"] = "test"
            b.save(default_setup)
            assert b.setup() == default_setup
            b.stop()

    def test_save_invalid(self):
        """
        Trying to save an invalid setup should raise ValidationError
        """
        with mock.patch("usb.core.find"):
            b = Backend()
        with pytest.raises(SetupValidator.ValidationError):
            b.save({})
        b.stop()

    def test_update(self):
        expected_data = {
            "bat": 0.0,
            "gear": 0,
            "iat": 0,
            "tps": 0,
            "ect": 0,
            "rpm": 0,
            "vss": 0,
            "o2": 0,
            "cam": 0,
            "mil": False,
            "fan": False,
            "bksw": False,
            "flr": False,
            "eth": 0,
            "scs": False,
            "fmw": "0.00",
            "map": 0,
            "an0": 104,
            "an1": 205.7905145,
            "an2": 205.7905145,
            "an3": 205.7905145,
            "an4": 205.7905145,
            "an5": 205.7905145,
            "an6": 205.7905145,
            "an7": 205.7905145,
            "time": "00:00:00",
            "odo": 0,
            "style": "day",
            "ver": "2.6.0",
        }

        with mock.patch("usb.core.find"), mock.patch(
            "usb.util.find_descriptor"
        ), mock.patch("backend.main.Websocket.__init__") as m_ws___init__, mock.patch(
            "threading.Thread.start"
        ):
            # mocking websocket
            m_ws___init__.return_value = None
            backend = Backend()

        assert backend.update() == expected_data
