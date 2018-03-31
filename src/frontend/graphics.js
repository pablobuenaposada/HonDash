var g1 = new JustGage({
    id: "g1",
    value: 0,
    min: 0,
    max: 20,
    decimals: 1,
    gaugeWidthScale: 1,
    label: "BATTERY",
    valueMinFontSize: 40,
 });

var g2 = new JustGage({
    id: "g2",
    value: 0,
    min: 0,
    max: 100,
    decimals: 0,
    gaugeWidthScale: 1,
    label: "IAT",
    valueMinFontSize: 50,
});

var g3 = new JustGage({
    id: "g3",
    value: 0,
    min: 0,
    max: 150,
    decimals: 0,
    gaugeWidthScale: 1,
    label: "ECT",
    valueMinFontSize: 50,
});

var g4 = new JustGage({
    id: "g4",
    value: 0,
    min: 0,
    max: 100,
    decimals: 1,
    gaugeWidthScale: 1,
    label: "AFR",
    valueMinFontSize: 50,
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

var g6 = new JustGage({
    id: "g6",
    value: 0,
    min: 0,
    max: 100,
    decimals: 0,
    gaugeWidthScale: 1,
    label: "temperature",
    valueMinFontSize: 50,
});

var g7 = new JustGage({
    id: "g7",
    value: 0,
    min: 0,
    max: 100,
    decimals: 0,
    gaugeWidthScale: 1,
    label: "temperature",
    valueMinFontSize: 50,
});

var g8 = new JustGage({
    id: "g8",
    value: 0,
    min: 0,
    max: 5,
    decimals: 2,
    gaugeWidthScale: 1,
    label: "ANALOG 0",
    valueMinFontSize: 50,
});

var clutch = new Bar("b1", 0, 0, false, "#edebeb", "purple", 0, 100, true, "%", "Arial", "bold", 20);
var brake = new Bar("b2", 0, 0, false, "#edebeb", "red", 0, 100, true, "%", "Arial", "bold", 20);
var throttle = new Bar("b3", 0, 0, false, "#edebeb", "green", 0, 100, true, "%", "Arial", "bold", 20);

var fuel = new Bar("fuel", 0, 0, true, "#edebeb", "orange", 0, 100, true, "%", "Arial", "bold", 20);
var rpm = new Text("rpm", "0", 100, "arial", "bold", "", " rpm");
var speed = new Text("speed", "0", 150, "arial", "bold", "", "");
var speed_unit = new Text("speed_unit", "km/h", 50, "arial", "bold", "", "");


//this.paper = Raphael("g1", "100%", "100%");
//this.text = this.paper.text(100, 30, "100C");
//this.text.attr({"font-family": "Verdana", "font-weight": "bold", "font-size": 50, "text-anchor": "middle"});
//this.text2 = this.paper.text(100, 60, "oil temp");
//this.text.attr({"font-family": "Verdana", "font-weight": "bold", "font-size": 50, "text-anchor": "end"});
