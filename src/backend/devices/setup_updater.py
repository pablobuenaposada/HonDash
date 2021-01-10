OLD_FORMULAS = [
    "autometer_2246",
    "ebay_150_psi",
    "civic_eg_fuel_tank",
    "civic_ek_fuel_tank",
    "s2000_fuel_tank",
    "mr2_w20_fuel_tank",
    "mr2_w30_fuel_tank",
    "mx5_na_fuel_tank",
]


class SetupUpdater:
    def update(self, setup):
        """Goes through all the versions and tries to update the setup"""
        if setup["version"] == "2.3.2":
            setup = self._update_to_2_4_0(setup)
        if setup["version"] == "2.4.0":
            setup = self._update_to_2_5_0(setup)
        if setup["version"] == "2.5.0":
            setup = self._update_to_2_6_0(setup)
        if setup["version"] == "2.6.0":
            setup = self._update_to_3_0_0(setup)
        if setup["version"] == "3.0.0":
            setup = self._update_to_3_1_0(setup)
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

    @staticmethod
    def _update_to_3_0_0(setup):
        """From 2.6.0 to 3.0.0"""
        setup["version"] = "3.0.0"
        setup.update({"name": {"tag": "ecu_name"}})
        return setup

    @staticmethod
    def _update_to_3_1_0(setup):
        """From 3.0.0 to 3.1.0"""
        setup["version"] = "3.1.0"
        for tag in setup:
            if tag[:2] == "an":
                setup[tag].update(
                    {
                        "min_voltage": 0,
                        "max_voltage": 5,
                        "min_value": 0,
                        "max_value": 100,
                    }
                )
            try:
                if setup[tag]["formula"] in OLD_FORMULAS:
                    setup[tag]["formula"] = "custom"
            except (TypeError, KeyError):
                pass
        return setup
