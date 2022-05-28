const SCREENS = ["basic.html", "animalillo.html", "datalogs"];
const DEBUG_SCREENS = ["debug/websocket.html", "debug/raw.html"];

function nextScreen(screens) {
  let path = window.location.pathname.split("/");
  path = path.filter(e => e); // remove empty strings

  let indexScreen = screens.findIndex(v => v.includes(path[path.length - 1]));
  indexScreen++;
  indexScreen = indexScreen % screens.length;

  let prefix = "/";
  if (window.location.host != "hondash.local") {
    prefix = "/src/frontend/";
  }

  window.location.pathname = prefix + screens[indexScreen];
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
