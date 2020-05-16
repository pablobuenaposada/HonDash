import json

import pytest

from backend.devices.setup_file import DEFAULT_CONFIG_FILE_NAME
from backend.devices.setup_validator.setup_validator import SetupValidator


class TestSetupValidator:
    def test_default(self):
        """Validate the default setup json"""
        with open(DEFAULT_CONFIG_FILE_NAME, "r") as setup_file:
            SetupValidator().validate(json.load(setup_file))

    def test_empty_json(self):
        """An empty json should fail validating"""
        with pytest.raises(SetupValidator.ValidationError) as excinfo:
            SetupValidator().validate({})
        assert str(excinfo.value) == "'ect' is a required property"

    def test__check_tag_uniqueness_success(self):
        SetupValidator()._check_tag_uniqueness(
            {"foo": {"tag": "tag1"}, "bar": {"tag": "tag2"}}
        )

    def test__check_tag_uniqueness_fail(self):
        """Repeated tags should fail"""
        with pytest.raises(SetupValidator.ValidationError) as excinfo:
            SetupValidator()._check_tag_uniqueness(
                {"foo": {"tag": "same_tag"}, "bar": {"tag": "same_tag"}}
            )
        assert str(excinfo.value) == "Repeated tag found"

    def test__check_formula_success(self):
        SetupValidator()._check_formula(
            {"foo": {"formula": "autometer_2246", "unit": "bar"}}
        )

    def test__check_formula_fail(self):
        """Invalid unit for specific formula should fail"""
        formula = "autometer_2246"
        unit = "celsius"
        with pytest.raises(SetupValidator.ValidationError) as excinfo:
            SetupValidator()._check_formula({"foo": {"formula": formula, "unit": unit}})
        assert str(excinfo.value) == f"{unit} not allowed for {formula}"

    def test__check_formula_no_formula_present(self):
        """If the value doesn't have formula then should validate correctly"""
        SetupValidator()._check_formula({"foo": {"bar"}})

    def test__check_formula_invalid_formula(self):
        """A formula not registered should fail"""
        formula = "fake_formula"
        with pytest.raises(SetupValidator.ValidationError) as excinfo:
            SetupValidator()._check_formula(
                {"foo": {"formula": formula, "unit": "bar"}}
            )
        assert str(excinfo.value) == f"{formula} not found"

    def test_validation_error(self):
        SetupValidator.ValidationError()