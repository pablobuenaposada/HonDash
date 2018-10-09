from unittest import TestCase

from devices.setup_file import SetupFile


class TestSetupFile(TestCase):

    def setUp(self):
        # note that the json file loaded in this test is the one used also as example
        # located in the root folder of this project
        self.setup = SetupFile()

    def test_get_value(self):
        """
        Checks that we can get the vss config values from the setup file
        """
        vss_params = self.setup.get_value('vss')
        assert vss_params  # checks that the dict return is not empty

    # def test_update_key(self):
    #     """
    #     Update of the label field for the vss config
    #     """
        # assert self.setup.get_value('vss')['label'] is ""
        # self.setup.update_key('vss', {'label': 'display text'})
        # assert self.setup.get_value('vss')['label'] is "display text"
