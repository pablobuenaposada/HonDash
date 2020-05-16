TEMP_UNITS = ["celsius", "fahrenheit"]
PRESSURE_UNITS = ["psi", "bar"]
PER_CENT_UNITS = ["per cent"]
SPEED_UNITS = ["kmh", "mph"]
DISTANCE_UNITS = ["km", "miles"]
MIXTURE_UNITS = ["afr", "lambda"]
TEMPLATES = ["basic", "animalillo"]
FORMULAS = [
    "autometer_2246",
    "vdo_323_057",
    "aem_30_2012",
    "ebay_150_psi",
    "bosch_0280130039_0280130026",
    "civic_eg_fuel_tank",
    "civic_ek_fuel_tank",
    "s2000_fuel_tank",
    "mr2_w20_fuel_tank",
    "mr2_w30_fuel_tank",
    "mx5_na_fuel_tank",
]
FORMULA_VS_UNITS = {
    "autometer_2246": PRESSURE_UNITS,
    "vdo_323_057": TEMP_UNITS,
    "aem_30_2012": TEMP_UNITS,
    "ebay_150_psi": PRESSURE_UNITS,
    "bosch_0280130039_0280130026": TEMP_UNITS,
    "civic_eg_fuel_tank": PER_CENT_UNITS,
    "civic_ek_fuel_tank": PER_CENT_UNITS,
    "s2000_fuel_tank": PER_CENT_UNITS,
    "mr2_w20_fuel_tank": PER_CENT_UNITS,
    "mr2_w30_fuel_tank": PER_CENT_UNITS,
    "mx5_na_fuel_tank": PER_CENT_UNITS,
}
TAGS = [
    "not use",
    "gauge1",
    "gauge2",
    "gauge3",
    "gauge4",
    "gauge5",
    "gauge6",
    "gauge7",
    "gauge8",
    "gauge9",
    "gauge10",
    "bar2",
]
FIELDS = [
    "ect",
    "vss",
    "ver",
    "fan",
    "eth",
    "mil",
    "odo",
    "map",
    "template",
    "o2",
    "gear",
    "style",
    "version",
    "iat",
    "tps",
    "screen",
    "rpm",
    "bat",
    "scs",
    "fmw",
    "time",
    "cam",
    "an0",
    "an1",
    "an2",
    "an3",
    "an4",
    "an5",
    "an6",
    "an7",
]


def icon(path_on, path_off, tag):
    return {
        "additionalProperties": False,
        "required": ["pathoff", "pathon", "tag"],
        "properties": {
            "pathoff": {"type": "string", "enum": [path_off]},
            "pathon": {"type": "string", "enum": [path_on]},
            "tag": {"type": "string", "enum": [tag]},
        },
    }


def analog():
    return {
        "additionalProperties": False,
        "required": ["tag", "unit", "formula"],
        "properties": {
            "tag": {"type": "string", "enum": TAGS},
            "formula": {"type": "string", "enum": FORMULAS},
            "unit": {
                "type": "string",
                "enum": TEMP_UNITS + PRESSURE_UNITS + PER_CENT_UNITS,
            },
            "decimals": {"type": "integer"},
            "label": {"type": "string"},
            "suffix": {"type": "string"},
            "max": {"type": "integer"},
            "sectors": {"type": "array", "items": {"$ref": "#/definitions/sector"}},
        },
    }


def simple_value_no_units(tags):
    schema = simple_value(tags)
    schema["required"].remove("unit")
    schema["properties"].pop("unit")
    return schema


def simple_value_no_decimals(tags, units):
    schema = simple_value(tags, units)
    schema["required"].remove("decimals")
    schema["properties"].pop("decimals")
    return schema


def simple_value_no_units_no_decimals(tags):
    schema = simple_value(tags)
    schema["required"].remove("unit")
    schema["properties"].pop("unit")
    schema["required"].remove("decimals")
    schema["properties"].pop("decimals")
    return schema


def simple_value(tags, units=None):
    return {
        "additionalProperties": False,
        "required": ["tag", "unit", "label", "suffix", "max", "sectors", "decimals"],
        "properties": {
            "tag": {"type": "string", "enum": tags},
            "unit": {"type": "string", "enum": units},
            "decimals": {"type": "integer"},
            "label": {"type": "string"},
            "suffix": {"type": "string"},
            "max": {"type": "integer"},
            "sectors": {"type": "array", "items": {"$ref": "#/definitions/sector"}},
        },
    }


SCHEMA = {
    "type": "object",
    "definitions": {
        "sector": {
            "additionalProperties": False,
            "required": ["lo", "hi", "color"],
            "properties": {
                "hi": {"type": "integer"},
                "lo": {"type": "integer"},
                "color": {"type": "string"},
            },
        },
    },
    "properties": {
        "ect": simple_value_no_decimals(TAGS, TEMP_UNITS),
        "vss": {
            "additionalProperties": False,
            "required": ["tag", "unit"],
            "properties": {
                "tag": {"type": "string", "enum": ["speed"]},
                "unit": {"type": "string", "enum": SPEED_UNITS},
            },
        },
        "ver": {
            "additionalProperties": False,
            "required": ["tag"],
            "properties": {"tag": {"type": "string", "enum": ["version"]}},
        },
        "fan": icon("fan_on.svg", "fan_off.svg", "icon2"),
        "eth": simple_value_no_units_no_decimals(TAGS),
        "mil": icon("check_engine_on.svg", "check_engine_off.svg", "icon1"),
        "odo": {
            "additionalProperties": False,
            "required": ["tag", "unit", "value"],
            "properties": {
                "tag": {"type": "string", "enum": ["odo"]},
                "unit": {"type": "string", "enum": DISTANCE_UNITS},
                "value": {"type": "integer"},
            },
        },
        "map": simple_value(TAGS, PRESSURE_UNITS),
        "template": {"type": "string", "enum": TEMPLATES},
        "o2": simple_value(TAGS, MIXTURE_UNITS),
        "gear": {
            "additionalProperties": False,
            "required": ["tag"],
            "properties": {"tag": {"type": "string", "enum": ["gear"]}},
        },
        "style": {
            "additionalProperties": False,
            "required": [
                "tag",
                "dayBackgroundColor",
                "dayBackgroundGaugeColor",
                "dayTextColor",
                "elapsedSeconds",
                "nightBackgroundColor",
                "nightBackgroundGaugeColor",
                "nightTextColor",
                "tpsLowerThreshold",
                "tpsUpperThreshold",
            ],
            "properties": {
                "dayBackgroundColor": {"type": "string"},
                "dayBackgroundGaugeColor": {"type": "string"},
                "dayTextColor": {"type": "string"},
                "elapsedSeconds": {"type": "integer"},
                "nightBackgroundColor": {"type": "string"},
                "nightBackgroundGaugeColor": {"type": "string"},
                "nightTextColor": {"type": "string"},
                "tag": {"type": "string", "enum": ["style"]},
                "tpsLowerThreshold": {"type": "integer"},
                "tpsUpperThreshold": {"type": "integer"},
            },
        },
        "version": {"type": "string"},
        "iat": simple_value_no_decimals(TAGS, TEMP_UNITS),
        "tps": simple_value_no_units_no_decimals(TAGS),
        "screen": {
            "additionalProperties": False,
            "required": ["rotate"],
            "properties": {"rotate": {"type": "boolean"}},
        },
        "rpm": {
            "additionalProperties": False,
            "required": ["tag"],
            "properties": {
                "tag": {"type": "string", "enum": ["bar1"]},
                "max": {"type": "integer"},
                "sectors": {"type": "array", "items": {"$ref": "#/definitions/sector"}},
            },
        },
        "bat": simple_value_no_units(TAGS),
        "scs": icon("scs_on.png", "scs_off.png", "icon3"),
        "fmw": {
            "additionalProperties": False,
            "required": ["tag"],
            "properties": {"tag": {"type": "string", "enum": ["firmware_version"]}},
        },
        "time": {
            "additionalProperties": False,
            "required": ["tag"],
            "properties": {"tag": {"type": "string", "enum": ["time"]}},
        },
        "cam": simple_value_no_units_no_decimals(TAGS),
        "an0": analog(),
        "an1": analog(),
        "an2": analog(),
        "an3": analog(),
        "an4": analog(),
        "an5": analog(),
        "an6": analog(),
        "an7": analog(),
    },
    "additionalProperties": False,
    "required": FIELDS,
}
