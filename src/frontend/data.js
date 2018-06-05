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
       speed.refresh(args[0]["vss"] || 0);
       gear.refresh(args[0]["gear"] || 0);
       icon1.refresh(args[0]["mil"] || 0);
       bar1.refresh(args[0]["rpm"] || 0);
       bar2.refresh(args[0]["an3"] || 0);
       gauge1.refresh(args[0]["ect"] || 0);
       gauge2.refresh(args[0]["iat"] || 0);
       gauge3.refresh(args[0]["an2"] || 0);
       gauge4.refresh(args[0]["an0"] || 0);
       gauge5.refresh(args[0]["an1"] || 0);
       gauge6.refresh(args[0]["bat"] || 0);
       gauge7.refresh(args[0]["cam"] || 0);
       gauge8.refresh(args[0]["o2"] || 0);
       gauge9.refresh(args[0]["map"] || 0);
       gauge10.refresh(args[0]["tps"] || 0);
       time.refresh(args[0]["time"] || 0);
       odometer.refresh(args[0]["odo"] || 0);
   }

   session.subscribe('com.app.idea', onevent1);
};

connection.open();
