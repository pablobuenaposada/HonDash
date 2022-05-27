const SCREENS = ["basic.html", "animalillo.html", "/datalogs/"];
const DEBUG_SCREENS = ["/debug/websocket.html", "/debug/raw.html"];

function nextScreen(screens) {
  let split = window.location.pathname.split(/\/frontend\//);
  let currentIndex = screens.indexOf(split[1]);
  currentIndex++;
  window.location.pathname =
    split[0] + "/frontend/" + screens[currentIndex % screens.length];
}

document.addEventListener("keydown", function(event) {
  if (event.key == "0") {
    ws.send(JSON.stringify({ action: "toggle_datalog" }));
  } else if (event.key == "1") {
    ws.send(JSON.stringify({ action: "toggle_style" }));
  } else if (event.key == "2") {
    nextScreen(SCREENS);
  } else if (event.key == "3") {
    nextScreen(DEBUG_SCREENS);
  }
});
