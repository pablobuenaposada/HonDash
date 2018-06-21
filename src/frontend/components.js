// Bars
var bar1 = new Bar({
    id: "bar1",
    isVertical: true,
    fillColor: "#d64d8a",
    maxValue: 9500,
    textEnding: "",
    textSize: 60
});

var bar2 = new Bar({
    id: "bar2",
    isVertical: true,
    fillColor: "#46877f",
    textSize: 30
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

var odometer = new Text({
    id: "odometer",
    value: "0",
    size: 3,
    style: "italic",
    suffix: " km"
});

// Icons
var icon1 = new Icon({
    id: "icon1",
    pathOff: "check_engine.svg",
    pathOn:  "check_engine_on.svg"
});

// Gauges
var gaugeDefaults = {
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

var gauge1 = new JustGage(Object.assign({}, gaugeDefaults, {
    id: "gauge1",
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

var gauge2 = new JustGage(Object.assign({}, gaugeDefaults, {
    id: "gauge2",
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

var gauge3 = new JustGage(Object.assign({}, gaugeDefaults, {
    id: "gauge3",
    max: 150,
    label: "OIL TEMP.",
    customSectors: {
        length: true,
        ranges: [{
            color : "#cc2c24",
            lo : 0,
            hi : 60
        },{
        color : "#46877f",
            lo : 60,
            hi : 95
        },{
        color : "#cc2c24",
            lo : 95,
            hi : 150
        }]
    }
}));

var gauge4 = new JustGage(Object.assign({}, gaugeDefaults, {
    id: "gauge4",
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

var gauge5 = new JustGage(Object.assign({}, gaugeDefaults, {
    id: "gauge5",
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

var gauge6 = new JustGage(Object.assign({}, gaugeDefaults, {
    id: "gauge6",
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

var gauge7 = new JustGage(Object.assign({}, gaugeDefaults, {
    id: "gauge7",
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

var gauge8 = new JustGage(Object.assign({}, gaugeDefaults, {
    id: "gauge8",
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

var gauge9 = new JustGage(Object.assign({}, gaugeDefaults, {
    id: "gauge9",
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

var gauge10 = new JustGage(Object.assign({}, gaugeDefaults, {
    id: "gauge10",
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