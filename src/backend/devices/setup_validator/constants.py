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
