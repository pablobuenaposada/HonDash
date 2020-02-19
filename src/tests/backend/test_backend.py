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
        Backend._instance = None  # we want to force new class instance

    def teardown_method(self):
        os.remove("setup.json")  # delete setup file
        subprocess.Popen(["venv/bin/crossbar", "stop"]).wait()  # close websocket
        Backend._instance = None  # we want to force new class instance

    def test_run_backend(self):
        with mock.patch("usb.core.find"), mock.patch(
            "devices.kpro.kpro.Kpro.__init__"
        ) as m___init__:
            # mocking kpro device since for tests is not available
            m___init__.return_value = None

            assert type(Backend.get()) == Backend

    def test_update(self):
        expected_data = {
            "bat": 0.0,
            "gear": "N",
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
            "ver": "2.3.2",
        }

        with mock.patch("usb.core.find"), mock.patch(
            "usb.util.find_descriptor"
        ), mock.patch("threading.Thread.start"), mock.patch(
            "backend.backend.publish"
        ) as m_publish:
            backend = Backend.get()
            backend.update()
            m_publish.assert_called_with("data", expected_data)
