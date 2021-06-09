import json
import os
from shutil import copyfile
from unittest import mock

import pytest

from backend.devices import setup_file
from backend.devices.formula import Formula
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
        ), mock.patch("backend.main.Websocket.__init__") as m_ws___init__:
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

    @pytest.mark.parametrize(
        "port, formula, unit, extra_params, expected_value",
        (
            (0, "aem_30_2012", "celsius", None, 149.2065268),
            (1, "vdo_323_057", "celsius", None, 205.7905145),
            (2, "bosch_0280130039_0280130026", "celsius", None, 104.9358479),
            (
                3,
                "custom",
                "bar",
                {
                    "min_voltage": 0.5,
                    "max_voltage": 4.5,
                    "min_value": 0,
                    "max_value": 100,
                },
                -12.5,
            ),
            (4, "aem_30_2012", "fahrenheit", None, 300.57174824000003),
            (5, "vdo_323_057", "fahrenheit", None, 402.4229261),
            (6, "bosch_0280130039_0280130026", "fahrenheit", None, 220.88452622),
            (
                7,
                "custom",
                "psi",
                {
                    "min_voltage": 0.5,
                    "max_voltage": 4.5,
                    "min_value": 0,
                    "max_value": 100,
                },
                -12.5,
            ),
        ),
    )
    def test__call_analog_input(
        self, port, formula, unit, extra_params, expected_value
    ):
        with mock.patch("usb.core.find"):
            b = Backend()
            setattr(b, f"an{port}_extra_params", extra_params)
            setattr(b, f"an{port}_formula", getattr(Formula, formula))
            setattr(b, f"an{port}_unit", unit)
        assert b._call_analog_input(port) == expected_value
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
            "an0": 0.0,
            "an1": 0.0,
            "an2": 0.0,
            "an3": 0.0,
            "an4": 0.0,
            "an5": 0.0,
            "an6": 0.0,
            "an7": 0.0,
            "time": "00:00:00",
            "odo": 0,
            "style": "day",
            "ver": "3.2.0",
            "name": "K-Pro",
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
