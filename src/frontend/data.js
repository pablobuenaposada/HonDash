var setup;

try {
  var autobahn = require("autobahn");
} catch (e) {
  // when running in browser, AutobahnJS will
  // be included without a module system
}

var webSocketUrl =
  "ws://" + (window.location.hostname || "hondash.local") + ":8080/ws";

var connection = new autobahn.Connection({
  url: webSocketUrl,
  realm: "realm1"
});

connection.onopen = function(session) {
  function onevent1(args) {
    for (var key in args[0]) {
      // for all values
      try {
        // if it's associated to a frontend tag
        window[setup[key]["tag"]]["refresh"](args[0][key]);
      } catch (e) {}
    }
  }

  function refresh(args) {
    location.reload();
  }

  session.call("setup").then(
    function(res) {
      setup = res;
      for (var value in setup) {
        for (var option in setup[value]) {
          var method = "set" + option.charAt(0).toUpperCase() + option.slice(1);
          try {
            window[setup[value]["tag"]][method](setup[value][option]);
          } catch (e) {
            // probably it´s not a field for setting up something in the frontend so we can skip it
          }
        }
      }
    },
    function(err) {
      // an error getting the setup? reload the page and try again
      location.reload();
    }
  );

  session.subscribe("data", onevent1);
  session.subscribe("refresh", refresh); // register a function for refreshing the frontend from the backend
};

connection.open();
