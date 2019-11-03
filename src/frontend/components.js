// Bars
var bar1 = new Bar({ id: "bar1", isVertical: true, textSize: 60 });
var bar2 = new Bar({ id: "bar2", isVertical: true, textSize: 30 });

// Text and numbers
var speed = new Text({ id: "speed", value: "0", size: 14 });
var gear = new Text({ id: "gear", value: "N", size: 14 });
var time = new Text({
  id: "time",
  value: "00:00:00",
  size: 4,
  style: "italic"
});
var odo = new Text({ id: "odo", value: "0", size: 3, style: "italic" });
var version = new Text({
  id: "version",
  value: "",
  size: 1,
  style: "italic",
  prefix: "HonDash v "
});
var firmware_version = new Text({
  id: "firmware_version",
  value: "",
  size: 1,
  style: "italic",
  prefix: "K-Pro v "
});

// Icons
var icon1 = new Icon({ id: "icon1" });
var icon2 = new Icon({ id: "icon2" });
var icon3 = new Icon({ id: "icon3" });

// Gauges
var gauge1 = new Gauge({ id: "gauge1" });
var gauge2 = new Gauge({ id: "gauge2" });
var gauge3 = new Gauge({ id: "gauge3" });
var gauge4 = new Gauge({ id: "gauge4" });
var gauge5 = new Gauge({ id: "gauge5" });
var gauge6 = new Gauge({ id: "gauge6" });
var gauge7 = new Gauge({ id: "gauge7" });
var gauge8 = new Gauge({ id: "gauge8" });
var gauge9 = new Gauge({ id: "gauge9" });
var gauge10 = new Gauge({ id: "gauge10" });

// Background
var style = new Style({ id: "style" });
