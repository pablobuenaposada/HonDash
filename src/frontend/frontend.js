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
       g6.refresh(args[0]["vss"]);
       g7.refresh(args[0]["vss"]);
       g8.refresh(args[0]["an0"]);
       clutch.refresh(args[0]["vss"]);
       brake.refresh(args[0]["vss"]);
       throttle.refresh(args[0]["tps"]);
       fuel.refresh(args[0]["vss"]);
       rpm.refresh(args[0]["rpm"]);
       speed.refresh(args[0]["vss"]);
       f.refresh(args[0]["h2o"]);
   }

   session.subscribe('com.app.idea', onevent1);
};

connection.open();



