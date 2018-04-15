var common_attr = {
    value: 0,
    gaugeWidthScale: 1,
    valueMinFontSize: 35,
    labelMinFontSize: 18,
    startAnimationTime: 0,
    refreshAnimationTime: 0,
    labelFontColor: "black",
};

// Bars
var clutch = new Bar("clutch", 0, 0, false, "#edebeb", "#2170a9", 0, 100, true, "%", "Arial", "bold", 20);
var brake = new Bar("brake", 0, 0, false, "#edebeb", "#cc2c24", 0, 100, true, "%", "Arial", "bold", 20);
var throttle = new Bar("throttle", 0, 0, false, "#edebeb", "#008b29", 0, 100, true, "%", "Arial", "bold", 20);
var fuel = new Bar("fuel", 0, 0, true, "#edebeb", "orange", 0, 100, true, "%", "Arial", "bold", 30);
var rpm = new Bar("rpm", 0, 0, true, "#edebeb", "#d64d8a", 0, 9500, true, "", "Arial", "bold", 60);

// Text and numbers
var speed = new Text("speed", "0", 8, "arial", "bold", "", "", "");
var speed_unit = new Text("speed_unit", "km/h", 2, "arial", "bold", "", "", "");
var gear = new Text("gear", "N", 10, "arial", "bold", "", "", "");
var time = new Text("time", "00:00:00", 3, "arial", "bold", "italic", "", "");
var odo = new Text("odo", "0", 2, "arial", "bold", "italic", "", " km");

// Icons
var reserve = new Icon("reserve", "fuel.svg");
var battery = new Icon("battery", "battery.svg");
var handbrake = new Icon("handbrake", "handbrake.svg");
var lights = new Icon("lights", "lights.svg");
var rear = new Icon("rear", "trunk.svg");
var engine = new Icon("engine", "check_engine.svg");
var oil = new Icon("oil", "oil.svg");
var leftarrow = new Icon("leftarrow", "left_arrow.svg", "left_arrow_on.svg");
var rightarrow = new Icon("rightarrow", "right_arrow.svg", "right_arrow_on.svg");

// Gauges
var bat = new JustGage(Object.assign({}, common_attr,
{
    id: "bat",
    min: 0,
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

var iat = new JustGage(Object.assign({}, common_attr,
{
    id: "iat",
    min: 0,
    max: 50,
    decimals: 0,
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

var ect = new JustGage(Object.assign({}, common_attr,
{
    id: "ect",
    min: 0,
    max: 150,
    decimals: 0,
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

var afr = new JustGage(Object.assign({}, common_attr,
{
    id: "afr",
    min: 0,
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

var cam = new JustGage(Object.assign({}, common_attr,
{
    id: "cam",
    min: 0,
    max: 100,
    decimals: 0,
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

var fuelp = new JustGage(Object.assign({}, common_attr,
{
    id: "fuelp",
    min: 0,
    max: 100,
    decimals: 0,
    label: "FUEL PRES.",
}));

var oilt = new JustGage(Object.assign({}, common_attr,
{
    id: "oilt",
    min: 0,
    max: 150,
    decimals: 0,
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

var oilp = new JustGage(Object.assign({}, common_attr,
{
    id: "oilp",
    min: 0,
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

var eth = new JustGage(Object.assign({}, common_attr,
{
    id: "eth",
    min: 0,
    max: 100,
    decimals: 0,
    label: "ETH",
}));

var g9 = new JustGage(Object.assign({}, common_attr,
{
    id: "g9",
    min: 0,
    max: 100,
    decimals: 0,
    label: "G9",
}));