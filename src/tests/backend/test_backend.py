import os
import subprocess
from shutil import copyfile
from unittest import mock

from backend.backend import Backend
from devices import setup_file


class TestBackend:
    def setup_method(self):
        # prepare the setup file where the backend expects it
        copyfile(setup_file.DEFAULT_CONFIG_FILE_NAME, setup_file.FILE_NAME)
        subprocess.Popen(["venv/bin/crossbar", "start"])  # start websocket

    def teardown_method(self):
        os.remove("setup.json")  # delete setup file
        subprocess.Popen(["venv/bin/crossbar", "stop"])  # close websocket

    def test_run_backend(self):
        with mock.patch("devices.kpro.kpro.Kpro.__init__") as m___init__:
            m___init__.return_value = (
                None  # mocking kpro device since for tests is not available
            )

        assert type(Backend.get()) == Backend

    def test_update(self):
        expected_data = {
            "bat": None,
            "gear": "N",
            "iat": 0,
            "tps": 0,
            "ect": 0,
            "rpm": None,
            "vss": 0,
            "o2": 0,
            "cam": None,
            "mil": False,
            "fan": None,
            "bksw": None,
            "flr": None,
            "eth": None,
            "scs": None,
            "fmw": 0,
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
            "ver": "2.3.1",
        }

        b = Backend.get()
        with mock.patch("backend.backend.publish") as m_publish:
            b.update()
            m_publish.assert_called_with("data", expected_data)
