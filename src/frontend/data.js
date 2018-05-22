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
       iat.refresh(args[0]["iat"]['celsius'] || 0);
       ect.refresh(args[0]["ect"]['celsius'] || 0);
       afr.refresh(args[0]["o2"]['afr'] || 0);
       mil.refresh(args[0]["mil"] || 0);
       map.refresh(args[0]["map"]['bar'] || 0);
       throttle.refresh(args[0]["tps"] || 0);
       cam.refresh(args[0]["cam"] || 0);
       rpm.refresh(args[0]["rpm"] || 0);
       speed.refresh(args[0]["vss"]['kmh'] || 0);
       time.refresh(args[0]["time"] || 0);
       odo.refresh(args[0]["odo"] || 0);
       gear.refresh(args[0]["gear"] || 0);
       oil_pressure.refresh(args[0]["an0"] || 0);
       fuel_pressure.refresh(args[0]["an1"] || 0);
       oil_temp.refresh(args[0]["an2"] || 0);
       fuel.refresh(args[0]["an3"] || 0);
       gear_temp.refresh(args[0]["an3"] || 0);
   }

   session.subscribe('com.app.idea', onevent1);
};

connection.open();
