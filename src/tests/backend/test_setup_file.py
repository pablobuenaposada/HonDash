from tempfile import NamedTemporaryFile

from devices import setup_file


class TestSetupFile:

    def setup_method(self):
        # note that the json file loaded in this test is the one used also as example
        # located in the root folder of this project
        self.setup = setup_file.SetupFile()

    def test_get_value(self):
        """
        Checks that we can get the vss config values from the setup file
        """
        vss_params = self.setup.get_value('vss')
        assert vss_params  # checks that the dict return is not empty

    def test_enable_rotate_screen(self):
        """
        Assuming that config.txt doesn't have the option enabled we are gonna activate it
        """
        with NamedTemporaryFile() as fp:
            setup_file.OS_CONFIG_FILE = fp.name

            assert fp.read() == b''  # clean config.txt

            self.setup.rotate_screen(True)

            assert fp.read() == b'display_rotate=2\n'  # now it contains the rotation option

    def test_enable_rotate_screen_already_enabled(self):
        """
        Assuming that config.txt has the option enabled we are gonna try to activate it again
        """
        with NamedTemporaryFile() as fp:
            fp.write(b'display_rotate=2\n')
            fp.flush()
            setup_file.OS_CONFIG_FILE = fp.name

            with open(fp.name) as f:
                assert f.read() == 'display_rotate=2\n'  # config.txt already contains this option

            self.setup.rotate_screen(True)

            with open(fp.name) as f:
                assert f.read() == 'display_rotate=2\n'  # no changes expected

    def test_disable_rotate_screen_already_disabled(self):
        """
        Assuming that config.txt doesn't have the option enabled we are gonna deactivate it
        """
        with NamedTemporaryFile() as fp:
            setup_file.OS_CONFIG_FILE = fp.name

            assert fp.read() == b''  # clean config.txt

            self.setup.rotate_screen(False)

            assert fp.read() == b''  # now it contains the rotation option

    def test_disable_rotate_screen(self):
        """
        Assuming that config.txt have the option enabled we are gonna deactivate it
        """
        with NamedTemporaryFile() as fp:
            fp.write(b'display_rotate=2\n')
            fp.flush()
            setup_file.OS_CONFIG_FILE = fp.name

            with open(fp.name) as f:
                assert f.read() == 'display_rotate=2\n'  # config.txt contains this option

            self.setup.rotate_screen(False)

            with open(fp.name) as f:
                assert f.read() == ''  # now is gone

    def test_update_key(self):
        """
        Check that an update of an attribute is performed but the rest is not
        """
        assert self.setup.get_value('vss')['label'] == ""
        self.setup.save_setup({"vss": {"label": "display text"}})
        assert self.setup.get_value('vss')['label'] == "display text"
        assert self.setup.get_value('screen') is not None
