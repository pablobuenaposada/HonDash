try {
   var autobahn = require('autobahn');
} catch (e) {
   // when running in browser, AutobahnJS will
   // be included without a module system
}

var connection = new autobahn.Connection({
   url: 'ws://127.0.0.1:8080/ws',
   realm: 'realm1'}
);

connection.onopen = function (session) {

   function onevent1(args) {
       bat.refresh(args[0]["bat"]);
       iat.refresh(args[0]["iat"]);
       ect.refresh(args[0]["ect"]);
       afr.refresh(args[0]["afr"]);
       cam.refresh(args[0]["cam"]);
       mil.refresh(args[0]["mil"]);
       fuel_pressure.refresh(args[0]["an1"]);
       oil_temp.refresh(args[0]["ai0"]);
       oil_pressure.refresh(args[0]["an0"]);
       clutch.refresh(args[0]["bksw"]);
       brake.refresh(args[0]["vss"]);
       throttle.refresh(args[0]["tps"]);
       fuel.refresh(args[0]["ai1"]);
       rpm.refresh(args[0]["rpm"]);
       speed.refresh(args[0]["vss"]);
       time.refresh(args[0]["time"]);
       odo.refresh(args[0]["odo"]);
       gear.refresh(args[0]["gear"])
       leftarrow.refresh(args[0]["di4"]);
       rightarrow.refresh(args[0]["di17"]);
       reserve.refresh(args[0]["di27"]);
       battery.refresh(args[0]["di22"]);
       mil.refresh(args[0]["mil"]);
       handbrake.refresh(args[0]["di12"]);
       high_beam.refresh(args[0]["di5"]);
       trunk.refresh(args[0]["di6"]);
       oil_warning.refresh(args[0]["di21"]);
   }

   session.subscribe('com.app.idea', onevent1);
};

connection.open();
