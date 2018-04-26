
// Bars
var clutch = new Bar({
    id: "clutch",
    backGroundColor: "#edebeb",
    fillColor: "#2170a9"
});

var brake = new Bar({ id: "brake", fillColor: "#cc2c24" });

var throttle = new Bar({ id: "throttle", fillColor: "#008b29" });

var fuel = new Bar({
    id: "fuel",
    isVertical: true,
    fillColor: "orange",
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
var speed = new Text({ id: "speed", value: "0", size: 8 });

var speed_unit = new Text({ id: "speed_unit", value: "km/h", size: 2 });

var gear = new Text({ id: "gear", value: "N", size: 10 });

var time = new Text({
    id: "time",
    value: "00:00:00",
    size: 3,
    style: "italic",
});

var odo = new Text({
    id: "odo",
    value: "0",
    size: 2,
    style: "italic",
    suffix: " km"
});

// Icons
var reserve = new Icon({
    id: "reserve",
    pathOff: "fuel.svg",
    pathOn: "fuel_on.svg"
});
var battery = new Icon({
    id: "battery",
    pathOff: "battery.svg",
    pathOn: "battery_on.svg"
});
var handbrake = new Icon({
    id: "handbrake",
    pathOff: "handbrake.svg",
    pathOn: "handbrake_on.svg"
});
var high_beam = new Icon({
    id: "high_beam",
    pathOff: "lights.svg",
    pathOn: "lights_on.svg"
});
var trunk = new Icon({
    id: "trunk",
    pathOff: "trunk.svg",
    pathOn: "trunk_on.svg"
});
var mil = new Icon({
    id: "mil",
    pathOff: "check_engine.svg",
    pathOn:  "check_engine_on.svg"
});
var oil_warning = new Icon({
    id: "oil_warning",
    pathOff: "oil.svg",
    pathOn: "oil_on.svg"
});
var leftarrow = new Icon({
    id: "leftarrow",
    pathOff: "left_arrow.svg",
    pathOn: "left_arrow_on.svg"
});
var rightarrow = new Icon({
    id: "rightarrow",
    pathOff: "right_arrow.svg",
    pathOn: "right_arrow_on.svg"
});

// Gauges
var gageDefaults = {
    min: 0,
    max: 100,
    value: 0,
    decimals: 0,
    gaugeWidthScale: 1,
    valueMinFontSize: 35,
    labelMinFontSize: 18,
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

var iat = new JustGage(Object.assign({}, gageDefaults, {
    id: "iat",
    max: 50,
    label: "IAT",
    customSectors: {
        length: true,
        ranges: [{
            color : "#cc2c24",
            lo : 30,
            hi : 50
        },{
        color : "#46877f",
            lo : 0,
            hi : 30
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
            lo : 90,
            hi : 150
        },{
        color : "#46877f",
            lo : 0,
            hi : 90
        }]
    }
}));

var afr = new JustGage(Object.assign({}, gageDefaults, {
    id: "afr",
    max: 2,
    decimals: 1,
    label: "AFR",
    customSectors: {
        length: true,
        ranges: [{
            color : "#cc2c24",
            lo : 0,
            hi : 0.9
        },{
        color : "#46877f",
            lo : 0.9,
            hi : 1.1
        },{
        color : "#cc2c24",
            lo : 1.1,
            hi : 2
        }]
    }
}));

var cam = new JustGage(Object.assign({}, gageDefaults, {
    id: "cam",
    label: "CAM",
    customSectors: {
        length: true,
        ranges: [{
            color : "#46877f",
            lo : 0,
            hi : 100
        }]
    }
}));

var fuelp = new JustGage(Object.assign({}, gageDefaults, {
    id: "fuelp",
    label: "FUEL PRES.",
}));

var oilt = new JustGage(Object.assign({}, gageDefaults, {
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

var oilp = new JustGage(Object.assign({}, gageDefaults, {
    id: "oilp",
    max: 5,
    decimals: 1,
    label: "OIL PRES.",
    customSectors: {
        length: true,
        ranges: [{
            color : "#cc2c24",
            lo : 0,
            hi : 2.5
        },{
        color : "#46877f",
            lo : 2.5,
            hi : 5
        }]
    }
}));

var eth = new JustGage(Object.assign({}, gageDefaults, {
    id: "eth",
    label: "ETH",
}));

var g9 = new JustGage(Object.assign({}, gageDefaults, {
    id: "g9",
    label: "G9",
}));