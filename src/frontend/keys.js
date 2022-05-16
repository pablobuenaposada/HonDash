const SCREENS = ["basic.html", "animalillo.html", "/datalogs/"];

document.addEventListener("keydown", function(event) {
  if (event.key == "0") {
    ws.send(JSON.stringify({ action: "toggle_datalog" }));
  } else if (event.key == "1") {
    ws.send(JSON.stringify({ action: "toggle_style" }));
  } else if (event.key == "2") {
    let split = window.location.pathname.split(/\/frontend\//);
    let currentIndex = SCREENS.indexOf(split[1]);
    currentIndex++;
    window.location.pathname =
      split[0] + "/frontend/" + SCREENS[currentIndex % SCREENS.length];
  }
});
