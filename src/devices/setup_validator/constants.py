TEMP_UNITS = ["celsius", "fahrenheit"]
PRESSURE_UNITS = ["psi", "bar"]
PER_CENT_UNITS = ["per cent"]
SPEED_UNITS = ["kmh", "mph"]
DISTANCE_UNITS = ["km", "miles"]
MIXTURE_UNITS = ["afr", "lambda"]
TEMPLATES = ["basic", "animalillo"]
FORMULAS = [
    "vdo_323_057",
    "aem_30_2012",
    "bosch_0280130039_0280130026",
    "custom",
]
FORMULA_VS_UNITS = {
    "vdo_323_057": TEMP_UNITS,
    "aem_30_2012": TEMP_UNITS,
    "bosch_0280130039_0280130026": TEMP_UNITS,
    "custom": TEMP_UNITS + PRESSURE_UNITS + PER_CENT_UNITS,
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
