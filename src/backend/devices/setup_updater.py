class SetupUpdater:
    def update(self, setup):
        """Goes through all the versions and tries to update the setup"""
        if setup["version"] == "2.3.2":
            setup = self._update_to_2_4_0(setup)
        if setup["version"] == "2.4.0":
            setup = self._update_to_2_5_0(setup)
        if setup["version"] == "2.5.0":
            setup = self._update_to_2_6_0(setup)
        return setup

    @staticmethod
    def _update_to_2_4_0(setup):
        """From 2.3.2 to 2.4.0"""
        del setup["vss"]["label"]
        del setup["vss"]["max"]
        del setup["vss"]["sectors"]
        del setup["vss"]["suffix"]
        setup["version"] = "2.4.0"
        return setup

    @staticmethod
    def _update_to_2_5_0(setup):
        """From 2.4.0 to 2.5.0"""
        setup["version"] = "2.5.0"
        return setup

    @staticmethod
    def _update_to_2_6_0(setup):
        """From 2.5.0 to 2.6.0"""
        setup["version"] = "2.6.0"
        return setup
