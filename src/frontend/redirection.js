var setup;

var setup = undefined;
var ws = new WebSocket(
  "ws://" + (window.location.hostname || "127.0.0.1") + ":5678/"
);

ws.onmessage = function(event) {
  var data = JSON.parse(event.data);
  var keys = Object.keys(data);

  // if the setup has not been received
  if (setup === undefined) {
    if (keys[0] == "setup") {
      setup = data["setup"];
      for (var value in setup) {
        for (var option in setup[value]) {
          var method = "set" + option.charAt(0).toUpperCase() + option.slice(1);
          try {
            window.location.replace(setup["template"] + ".html");
          } catch (e) {
            // probably it´s not a field for setting up something in the frontend so we can skip it
          }
        }
      }
    }
  }
};

// asks for the setup as soon as possible
ws.onopen = function(e) {
  ws.send(JSON.stringify({ action: "setup" }));
};

// in case something blows up or connection gets closed, keep trying
ws.onerror = function(e) {
  location.reload();
};
ws.onclose = function(e) {
  location.reload();
};
