import os
from shutil import copyfile
from tempfile import NamedTemporaryFile

from devices import setup_file
from devices.formula import Formula


def setup_method(self):
    # note that the json file loaded in this test is the one used also as example
    # located in the root folder of this project
    self.file_name = NamedTemporaryFile().name
    copyfile(setup_file.DEFAULT_CONFIG_FILE_NAME, self.file_name)
    self.setup = setup_file.SetupFile(self.file_name)


def teardown_method(self):
    os.remove(self.file_name)


class TestRotateScreen:
    def setup_method(self):
        setup_method(self)

    def teardown_method(self):
        teardown_method(self)

    def test_enable_rotate_screen(self):
        """
        Assuming that config.txt doesn't have the option enabled we are gonna activate it
        """
        with NamedTemporaryFile() as fp:
            setup_file.OS_CONFIG_FILE = fp.name

            assert fp.read() == b""  # clean config.txt

            self.setup.rotate_screen(True)

            assert (
                fp.read() == b"display_rotate=2\n"
            )  # now it contains the rotation option

    def test_enable_rotate_screen_already_enabled(self):
        """
        Assuming that config.txt has the option enabled we are gonna try to activate it again
        """
        with NamedTemporaryFile() as fp:
            fp.write(b"display_rotate=2\n")
            fp.flush()
            setup_file.OS_CONFIG_FILE = fp.name

            with open(fp.name) as f:
                assert (
                    f.read() == "display_rotate=2\n"
                )  # config.txt already contains this option

            self.setup.rotate_screen(True)

            with open(fp.name) as f:
                assert f.read() == "display_rotate=2\n"  # no changes expected

    def test_disable_rotate_screen_already_disabled(self):
        """
        Assuming that config.txt doesn't have the option enabled we are gonna deactivate it
        """
        with NamedTemporaryFile() as fp:
            setup_file.OS_CONFIG_FILE = fp.name

            assert fp.read() == b""  # clean config.txt

            self.setup.rotate_screen(False)

            assert fp.read() == b""  # now it contains the rotation option

    def test_disable_rotate_screen(self):
        """
        Assuming that config.txt have the option enabled we are gonna deactivate it
        """
        with NamedTemporaryFile() as fp:
            fp.write(b"display_rotate=2\n")
            fp.flush()
            setup_file.OS_CONFIG_FILE = fp.name

            with open(fp.name) as f:
                assert (
                    f.read() == "display_rotate=2\n"
                )  # config.txt contains this option

            self.setup.rotate_screen(False)

            with open(fp.name) as f:
                assert f.read() == ""  # now is gone


class TestSetupFile:
    def setup_method(self):
        setup_method(self)

    def teardown_method(self):
        teardown_method(self)

    def test_get_value(self):
        """
        Checks that we can get the vss config values from the setup file
        """
        vss_params = self.setup.get_value("vss")
        assert vss_params  # checks that the dict return is not empty

    def test_reset_setup(self):
        """ Checks that the reset setup loads the default json """
        # get the initial value for vss
        vss_config = self.setup.get_value("vss")

        # let's put the json in blank
        self.setup.json = {}
        assert self.setup.get_value("vss") is None

        # reset the setup
        self.setup.reset_setup()

        # now the value should be back
        assert self.setup.get_value("vss") == vss_config

    def test_save_setup(self):
        """
        Check that an update of an attribute is performed but the rest is not
        """
        assert self.setup.get_value("tps")["label"] == "TPS"
        self.setup.save_setup({"tps": {"label": "display text"}})
        assert self.setup.get_value("tps")["label"] == "display text"
        assert self.setup.get_value("screen") is not None

    def test_update_key(self):
        assert self.setup.get_value("tps") == {
            "label": "TPS",
            "max": 100,
            "sectors": [{"color": "#46877f", "hi": 100, "lo": 0}],
            "suffix": "",
            "tag": "gauge8",
        }
        self.setup.update_key("tps", {"label": "foo"})
        assert self.setup.get_value("tps") == {
            "label": "foo",
            "max": 100,
            "sectors": [{"color": "#46877f", "hi": 100, "lo": 0}],
            "suffix": "",
            "tag": "gauge8",
        }

    def test_get_formula_non_existent(self):
        """If not formula found return voltage one"""
        assert self.setup.get_formula(None) == Formula.voltage
