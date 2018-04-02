var bat = new JustGage({
    id: "bat",
    value: 0,
    min: 0,
    max: 20,
    decimals: 1,
    gaugeWidthScale: 1,
    label: "BATTERY",
    valueMinFontSize: 40,
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
    valueMinFontSize: 50,
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
});

var fuelp = new JustGage({
    id: "fuelp",
    value: 0,
    min: 0,
    max: 100,
    decimals: 0,
    gaugeWidthScale: 1,
    label: "FUEL PRESSURE",
    valueMinFontSize: 50,
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
});

var oilp = new JustGage({
    id: "oilp",
    value: 0,
    min: 0,
    max: 5,
    decimals: 2,
    gaugeWidthScale: 1,
    label: "OIL PRESSURE",
    valueMinFontSize: 50,
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

var clutch = new Bar("b1", 0, 0, false, "#edebeb", "purple", 0, 100, true, "%", "Arial", "bold", 20);
var brake = new Bar("b2", 0, 0, false, "#edebeb", "red", 0, 100, true, "%", "Arial", "bold", 20);
var throttle = new Bar("b3", 0, 0, false, "#edebeb", "#008b29", 0, 100, true, "%", "Arial", "bold", 20);

var fuel = new Bar("fuel", 0, 0, true, "#edebeb", "orange", 0, 100, true, "%", "Arial", "bold", 20);
var rpm = new Bar("rpm", 0, 0, true, "#edebeb", "#bc4077", 0, 9500, true, "", "Arial", "bold", 40);

var speed = new Text("speed", "0", 150, "arial", "bold", "", "");
var speed_unit = new Text("speed_unit", "km/h", 50, "arial", "bold", "", "");
var gear = new Text("gear", "N", 150, "arial", "bold", "", "");

//this.paper = Raphael("g1", "100%", "100%");
//this.text = this.paper.text(100, 30, "100C");
//this.text.attr({"font-family": "Verdana", "font-weight": "bold", "font-size": 50, "text-anchor": "middle"});
//this.text2 = this.paper.text(100, 60, "oil temp");
//this.text.attr({"font-family": "Verdana", "font-weight": "bold", "font-size": 50, "text-anchor": "end"});
