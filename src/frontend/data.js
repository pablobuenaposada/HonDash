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
       g5.refresh(args[0]["cam"]);
       fuelp.refresh(args[0]["vss"]);
       oilt.refresh(args[0]["vss"]);
       oilp.refresh(args[0]["an0"]);
       clutch.refresh(args[0]["vss"]);
       brake.refresh(args[0]["vss"]);
       throttle.refresh(args[0]["tps"]);
       fuel.refresh(args[0]["tps"]);
       rpm.refresh(args[0]["rpm"]);
       speed.refresh(args[0]["vss"]);
       time.refresh(args[0]["time"]);
       odo.refresh(args[0]["odo"]);
       gear.refresh(args[0]["gear"])
       leftarrow.refresh(args[0]["left_turn_signal"]);
       rightarrow.refresh(args[0]["right_turn_signal"]);
   }

   session.subscribe('com.app.idea', onevent1);
};

connection.open();