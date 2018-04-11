var labelSize = 15;

var bat = new JustGage({
    id: "bat",
    value: 0,
    min: 0,
    max: 20,
    decimals: 1,
    gaugeWidthScale: 1,
    label: "BATTERY",
    valueMinFontSize: 40,
    labelMinFontSize: labelSize,
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
 });

var iat = new JustGage({
    id: "g2",
    value: 0,
    min: 0,
    max: 50,
    decimals: 0,
    gaugeWidthScale: 1,
    label: "IAT",
    valueMinFontSize: 50,
    labelMinFontSize: labelSize,
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
});

var ect = new JustGage({
    id: "g3",
    value: 0,
    min: 0,
    max: 150,
    decimals: 0,
    gaugeWidthScale: 1,
    label: "ECT",
    valueMinFontSize: 50,
    labelMinFontSize: labelSize,
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
});

var afr = new JustGage({
    id: "g4",
    value: 0,
    min: 0,
    max: 2,
    decimals: 1,
    gaugeWidthScale: 1,
    label: "AFR",
    valueMinFontSize: 40,
    labelMinFontSize: labelSize,
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
});

var g5 = new JustGage({
    id: "g5",
    value: 0,
    min: 0,
    max: 100,
    decimals: 0,
    gaugeWidthScale: 1,
    label: "CAM",
    valueMinFontSize: 50,
    labelMinFontSize: labelSize,
});

var fuelp = new JustGage({
    id: "fuelp",
    value: 0,
    min: 0,
    max: 100,
    decimals: 0,
    gaugeWidthScale: 1,
    label: "FUEL PRESS.",
    valueMinFontSize: 50,
    labelMinFontSize: labelSize,
});

var oilt = new JustGage({
    id: "oilt",
    value: 0,
    min: 0,
    max: 100,
    decimals: 0,
    gaugeWidthScale: 1,
    label: "OIL TEMP",
    valueMinFontSize: 50,
    labelMinFontSize: labelSize,
});

var oilp = new JustGage({
    id: "oilp",
    value: 0,
    min: 0,
    max: 5,
    decimals: 1,
    gaugeWidthScale: 1,
    label: "OIL PRESS.",
    valueMinFontSize: 40,
    labelMinFontSize: labelSize,
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
});

var eth = new JustGage({
    id: "eth",
    value: 0,
    min: 0,
    max: 100,
    decimals: 0,
    gaugeWidthScale: 1,
    label: "ETH",
    valueMinFontSize: 50,
    labelMinFontSize: labelSize,
});

var g7 = new JustGage({
    id: "g7",
    value: 0,
    min: 0,
    max: 100,
    decimals: 0,
    gaugeWidthScale: 1,
    label: "G7",
    valueMinFontSize: 50,
    labelMinFontSize: labelSize,
});

var g8 = new JustGage({
    id: "g8",
    value: 0,
    min: 0,
    max: 100,
    decimals: 0,
    gaugeWidthScale: 1,
    label: "G8",
    valueMinFontSize: 50,
    labelMinFontSize: labelSize,
});

var g9 = new JustGage({
    id: "g9",
    value: 0,
    min: 0,
    max: 100,
    decimals: 0,
    gaugeWidthScale: 1,
    label: "G9",
    valueMinFontSize: 50,
    labelMinFontSize: labelSize,

});

var clutch = new Bar("b1", 0, 0, false, "#edebeb", "#222d5a", 0, 100, true, "%", "Arial", "bold", 20);
var brake = new Bar("b2", 0, 0, false, "#edebeb", "#cc2c24", 0, 100, true, "%", "Arial", "bold", 20);
var throttle = new Bar("b3", 0, 0, false, "#edebeb", "#008b29", 0, 100, true, "%", "Arial", "bold", 20);

var fuel = new Bar("fuel", 0, 0, true, "#edebeb", "orange", 0, 100, true, "%", "Arial", "bold", 30);
var rpm = new Bar("rpm", 0, 0, true, "#edebeb", "#bc4077", 0, 9500, true, "", "Arial", "bold", 60);

var speed = new Text("speed", "0", 8, "arial", "bold", "", "", "");
var speed_unit = new Text("speed_unit", "km/h", 2, "arial", "bold", "", "", "");
var gear = new Text("gear", "N", 10, "arial", "bold", "", "", "");

var time = new Text("time", "00:00:00", 2, "arial", "bold", "italic", "", "");
var odo = new Text("odo", "0", 2, "arial", "bold", "italic", "", " km");

var reserve = new Icon("reserve", "fuel.svg");
var battery = new Icon("battery", "battery.svg");
var handbrake = new Icon("handbrake", "handbrake.svg");
var lights = new Icon("lights", "lights.svg");
var rear = new Icon("rear", "trunk.svg");
var engine = new Icon("engine", "check_engine.svg");
var oil = new Icon("oil", "oil.svg");
var leftarrow = new Icon("leftarrow", "left_arrow.svg", "left_arrow_on.svg");
var rightarrow = new Icon("rightarrow", "right_arrow.svg", "right_arrow_on.svg");