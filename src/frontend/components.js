// Bars
var fuel = new Bar({
    id: "fuel",
    isVertical: true,
    fillColor: "#46877f",
    textSize: 30
});

var rpm = new Bar({
    id: "rpm",
    isVertical: true,
    fillColor: "#d64d8a",
    maxValue: 9500,
    textEnding: "",
    textSize: 60
});

// Text and numbers
var speed = new Text({ id: "speed", value: "0", size: 14 });

var speed_unit = new Text({ id: "speed_unit", value: "km/h", size: 3 });

var gear = new Text({ id: "gear", value: "N", size: 14 });

var time = new Text({
    id: "time",
    value: "00:00:00",
    size: 4,
    style: "italic",
});

var odo = new Text({
    id: "odo",
    value: "0",
    size: 3,
    style: "italic",
    suffix: " km"
});

// Icons
var mil = new Icon({
    id: "mil",
    pathOff: "check_engine.svg",
    pathOn:  "check_engine_on.svg"
});

// Gauges
var gageDefaults = {
    min: 0,
    max: 100,
    value: 0,
    decimals: 0,
    gaugeWidthScale: 1,
    valueMinFontSize: 60,
    labelMinFontSize: 20,
    startAnimationTime: 0,
    refreshAnimationTime: 0,
    labelFontColor: "black",
};

var bat = new JustGage(Object.assign({}, gageDefaults, {
    id: "bat",
    max: 20,
    decimals: 1,
    label: "BATTERY",
    customSectors: {
        length: true,
        ranges: [{
            color : "#cc2c24",
            lo : 0,
            hi : 12
        },{
        color : "#46877f",
            lo : 12,
            hi : 20
        }]
    }
}));

var throttle = new JustGage(Object.assign({}, gageDefaults, {
    id: "tps",
    label: "TPS",
    customSectors: {
        length: true,
        ranges: [{
        color : "#46877f",
            lo : 0,
            hi : 100
        }]
    }
}));

var iat = new JustGage(Object.assign({}, gageDefaults, {
    id: "iat",
    max: 50,
    label: "IAT",
    customSectors: {
        length: true,
        ranges: [{
        color : "#46877f",
            lo : 0,
            hi : 50
        }]
    }
}));

var ect = new JustGage(Object.assign({}, gageDefaults, {
    id: "ect",
    max: 150,
    label: "ECT",
    customSectors: {
        length: true,
        ranges: [{
            color : "#cc2c24",
            lo : 94,
            hi : 150
        },{
        color : "#46877f",
            lo : 0,
            hi : 93
        }]
    }
}));

var afr = new JustGage(Object.assign({}, gageDefaults, {
    id: "afr",
    max: 30,
    decimals: 1,
    label: "AFR",
    customSectors: {
        length: true,
        ranges: [{
            color : "#cc2c24",
            lo : 0,
            hi : 12.0
        },{
        color : "#46877f",
            lo : 12.0,
            hi : 16.0
        },{
        color : "#cc2c24",
            lo : 16.0,
            hi : 30
        }]
    }
}));

var fuel_pressure = new JustGage(Object.assign({}, gageDefaults, {
    id: "fuelp",
    label: "FUEL PRES.",
    customSectors: {
        length: true,
        ranges: [{
            color : "#46877f",
            lo : 0,
            hi : 100
        }]
    }
}));

var oil_temp = new JustGage(Object.assign({}, gageDefaults, {
    id: "oilt",
    max: 150,
    label: "OIL TEMP.",
    customSectors: {
        length: true,
        ranges: [{
            color : "#cc2c24",
            lo : 0,
            hi : 80
        },{
        color : "#46877f",
            lo : 80,
            hi : 95
        },{
        color : "#cc2c24",
            lo : 95,
            hi : 150
        }]
    }
}));

var cam = new JustGage(Object.assign({}, gageDefaults, {
    id: "cam",
    max: 150,
    label: "CAM",
    customSectors: {
        length: true,
        ranges: [{
        color : "#46877f",
            lo : 0,
            hi : 50
        }]
    }
}));

var oil_pressure = new JustGage(Object.assign({}, gageDefaults, {
    id: "oilp",
    max: 7,
    decimals: 1,
    label: "OIL PRES.",
    customSectors: {
        length: true,
        ranges: [{
            color : "#cc2c24",
            lo : 0,
            hi : 2
        },{
        color : "#46877f",
            lo : 2,
            hi : 7
        }]
    }
}));

var map = new JustGage(Object.assign({}, gageDefaults, {
    id: "map",
    max: 3,
    decimals: 1,
    label: "MAP",
    customSectors: {
        length: true,
        ranges: [{
            color : "#46877f",
            lo : 0,
            hi : 3
        }]
    }
}));