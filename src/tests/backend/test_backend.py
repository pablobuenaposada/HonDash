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
            b = Backend.get()

        assert type(b) == Backend
