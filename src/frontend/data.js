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
       bat.refresh(args[0]["bat"] || 0);
       iat.refresh(args[0]["iat"] || 0);
       ect.refresh(args[0]["ect"] || 0);
       afr.refresh(args[0]["afr"] || 0);
       cam.refresh(args[0]["cam"] || 0);
       mil.refresh(args[0]["mil"] || 0);
       map.refresh(args[0]["map"] || 0);
       fuel_pressure.refresh(args[0]["an1"] || 0);
       oil_temp.refresh(args[0]["ai0"] || 0);
       oil_pressure.refresh(args[0]["an0"] || 0);
       clutch.refresh(args[0]["bksw"] || 0);
       brake.refresh(args[0]["vss"] || 0);
       throttle.refresh(args[0]["tps"] || 0);
       fuel.refresh(args[0]["ai1"] || 0);
       rpm.refresh(args[0]["rpm"] || 0);
       speed.refresh(args[0]["vss"] || 0);
       time.refresh(args[0]["time"] || 0);
       odo.refresh(args[0]["odo"] || 0);
       gear.refresh(args[0]["gear"] || 0)
       leftarrow.refresh(args[0]["di4"] || 0);
       rightarrow.refresh(args[0]["di17"] || 0);
       reserve.refresh(args[0]["di27"] || 0);
       battery.refresh(args[0]["di22"] || 0);
       handbrake.refresh(args[0]["di12"] || 0);
       high_beam.refresh(args[0]["di5"] || 0);
       trunk.refresh(args[0]["di6"] || 0);
       oil_warning.refresh(args[0]["di21"] || 0);
   }

   session.subscribe('com.app.idea', onevent1);
};

connection.open();
