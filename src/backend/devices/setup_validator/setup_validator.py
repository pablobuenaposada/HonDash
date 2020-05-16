import jsonschema

from backend.devices.setup_validator.constants import FORMULA_VS_UNITS, SCHEMA


class SetupValidator:
    def validate(self, setup):
        try:
            jsonschema.validate(instance=setup, schema=SCHEMA)
        except jsonschema.exceptions.ValidationError as e:
            raise self.ValidationError(e.message)
        self._check_version(setup)
        self._check_tag_uniqueness(setup)
        self._check_formula(setup)

    def _check_tag_uniqueness(self, setup):
        """tag values should be unique"""
        tags = []
        for value in setup:
            try:
                tags.append(setup[value]["tag"])
            except (KeyError, TypeError):  # if tag is not present it's fine
                pass
        tags = [
            tag for tag in tags if tag != "not use"
        ]  # delete "not use" tags for this check
        if len(tags) > len(
            set(tags)
        ):  # casting to set we delete duplicates so then we can compare
            raise self.ValidationError("Repeated tag found")

    def _check_formula(self, setup):
        for value in setup:
            try:
                formula = setup[value]["formula"]
            except (KeyError, TypeError):  # if formula is not present it's fine
                break
            try:
                allowed_units = FORMULA_VS_UNITS[formula]
            except KeyError:
                raise self.ValidationError(f"{setup[value]['formula']} not found")
            if setup[value]["unit"] not in allowed_units:
                raise self.ValidationError(
                    f"{setup[value]['unit']} not allowed for {setup[value]['formula']}"
                )

    def _check_version(self, setup):
        if setup["version"] != "2.4.0":
            raise self.ValidationError("setup file should be version 2.4.0")

    class ValidationError(Exception):
        def __init__(self, *args):
            if args:
                self.message = args[0]
