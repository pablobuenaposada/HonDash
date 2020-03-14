function internal_grid() {
  return { grid_columns: 12 };
}

function external_grid() {
  return { grid_columns: 4 };
}

/* units */
var temp_units = ["celsius", "fahrenheit"];
var speed_units = ["kmh", "mph"];
var mixture_units = ["afr", "lambda"];
var pressure_units = ["psi", "bar"];
var per_cent_units = ["per cent"];
var distance_units = ["km", "miles"];

/* util functions */
function unit(units) {
  return { type: "string", enum: units, options: internal_grid() };
}
function simple_value_no_units() {
  var config = simple_value();
  delete config["required"].splice(1);
  delete config["properties"]["unit"];
  return config;
}
function simple_value_no_units_no_decimals() {
  var config = simple_value_no_units();
  delete config["properties"]["decimals"];
  return config;
}
function simple_value_no_decimals(units) {
  var config = simple_value(units);
  delete config["properties"]["decimals"];
  return config;
}
function simple_value(units) {
  return {
    type: "object",
    required: ["tag", "unit"],
    options: external_grid(),
    properties: {
      tag: tag,
      unit: unit(units),
      decimals: decimals,
      label: label,
      suffix: suffix,
      max: max,
      sectors: sectors
    }
  };
}

/* fields */
var tag = {
  type: "string",
  options: internal_grid(),
  enum: [
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
    "time",
    "odo",
    "bar1",
    "bar2",
    "icon1",
    "icon2",
    "icon3",
    "gear",
    "speed"
  ]
};
var formula = {
  type: "string",
  options: internal_grid(),
  enum: [
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
    "mx5_na_fuel_tank"
  ]
};
var time = {
  type: "object",
  required: ["tag"],
  properties: {
    tag: tag
  },
  options: external_grid()
};
var screen = {
  type: "object",
  required: ["rotate"],
  properties: {
    rotate: {
      type: "boolean",
      options: internal_grid()
    }
  },
  options: external_grid()
};
var sectors = {
  type: "array",
  format: "table",
  items: {
    type: "object",
    options: internal_grid(),
    properties: {
      lo: {
        type: "integer"
      },
      hi: {
        type: "integer"
      },
      color: {
        type: "string",
        format: "color"
      }
    }
  }
};
var odo = {
  type: "object",
  required: ["tag", "unit"],
  options: external_grid(),
  properties: {
    tag: tag,
    unit: unit(distance_units),
    suffix: suffix,
    value: { type: "number", options: internal_grid() }
  }
};
var rpm = {
  type: "object",
  required: ["tag"],
  options: external_grid(),
  properties: {
    tag: tag,
    suffix: suffix,
    max: { type: "integer", options: internal_grid() }, // this fucker should use the max var but doesn't work
    sectors: sectors
  }
};
var mil = {
  type: "object",
  required: ["tag"],
  options: external_grid(),
  properties: {
    tag: tag,
    pathon: { type: "string", options: internal_grid() },
    pathoff: { type: "string", options: internal_grid() }
  }
};
var fan = {
  type: "object",
  required: ["tag"],
  options: external_grid(),
  properties: {
    tag: tag,
    pathon: { type: "string", options: internal_grid() },
    pathoff: { type: "string", options: internal_grid() }
  }
};
var scs = {
  type: "object",
  required: ["tag"],
  options: external_grid(),
  properties: {
    tag: tag,
    pathon: { type: "string", options: internal_grid() },
    pathoff: { type: "string", options: internal_grid() }
  }
};
var gear = {
  type: "object",
  required: ["tag"],
  options: external_grid(),
  properties: {
    tag: tag
  }
};
var template = {
  type: "string",
  required: true,
  enum: ["basic", "animalillo"],
  options: external_grid(),
  links: [{ mediaType: "image", href: "templates/{{self}}.png" }]
};
var label = { type: "string", options: internal_grid() };
var max = { type: "integer", options: internal_grid() };
var decimals = { type: "integer", options: internal_grid() };
var suffix = { type: "string", options: internal_grid() };
var analog = {
  type: "object",
  required: ["tag", "unit", "formula"],
  options: external_grid(),
  properties: {
    tag: tag,
    formula: formula,
    unit: unit(temp_units.concat(pressure_units).concat(per_cent_units)),
    decimals: decimals,
    label: label,
    suffix: suffix,
    max: max,
    sectors: sectors
  }
};
var style = {
  type: "object",
  required: [
    "tag",
    "dayBackgroundColor",
    "nightBackgroundColor",
    "dayTextColor",
    "nightTextColor",
    "dayBackgroundGaugeColor",
    "nightBackgroundGaugeColor",
    "tpsLowerThreshold",
    "tpsUpperThreshold",
    "elapsedSeconds"
  ],
  properties: {
    tag: {
      type: "string",
      enum: ["style"]
    },
    dayBackgroundColor: {
      type: "string",
      format: "color",
      options: internal_grid()
    },
    nightBackgroundColor: {
      type: "string",
      format: "color",
      options: internal_grid()
    },
    dayTextColor: {
      type: "string",
      format: "color",
      options: internal_grid()
    },
    nightTextColor: {
      type: "string",
      format: "color",
      options: internal_grid()
    },
    dayBackgroundGaugeColor: {
      type: "string",
      format: "color",
      options: internal_grid()
    },
    nightBackgroundGaugeColor: {
      type: "string",
      format: "color",
      options: internal_grid()
    },
    tpsLowerThreshold: {
      type: "integer",
      options: internal_grid()
    },
    tpsUpperThreshold: {
      type: "integer",
      options: internal_grid()
    },
    elapsedSeconds: {
      type: "integer",
      options: internal_grid()
    }
  },
  options: external_grid()
};

var schema = {
  schema: {
    type: "object",
    title: "HonDash setup",
    hideTitle: true,
    properties: {
      template: template,
      screen: screen,
      time: time,
      style: style,
      odo: odo,
      gear: gear,
      rpm: rpm,
      mil: mil,
      fan: fan,
      scs: scs,
      eth: simple_value_no_units_no_decimals(),
      vss: simple_value_no_decimals(speed_units),
      cam: simple_value_no_units_no_decimals(),
      bat: simple_value_no_units(),
      tps: simple_value_no_units_no_decimals(),
      iat: simple_value_no_decimals(temp_units),
      ect: simple_value_no_decimals(temp_units),
      o2: simple_value(mixture_units),
      map: simple_value(pressure_units),
      an0: analog,
      an1: analog,
      an2: analog,
      an3: analog,
      an4: analog,
      an5: analog,
      an6: analog,
      an7: analog
    }
  },
  no_additional_properties: true,
  disable_collapse: true,
  disable_edit_json: true,
  disable_properties: true,
  disable_array_delete_last_row: true,
  disable_array_reorder: true,
  theme: "bootstrap4",
  object_layout: "grid"
};
