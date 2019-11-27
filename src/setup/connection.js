function getElementsByXPath(xpath, parent) {
  let results = [];
  let query = document.evaluate(
    xpath,
    parent || document,
    null,
    XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
    null
  );
  for (let i = 0, length = query.snapshotLength; i < length; ++i) {
    results.push(query.snapshotItem(i));
  }
  return results;
}

function disableField(xpath) {
  getElementsByXPath(xpath)[0].disabled = true;
}

function disableFromSelectByValue(select, value) {
  for (var option in select[0].options) {
    if (select[0].options[option].label == value) {
      select[0].options[option].disabled = true;
      break;
    }
  }
}

function checkTagValues() {
  // get currently used tags
  var usedTags = [];
  var divs = getElementsByXPath(
    "//*[@id='editor_holder']/div/div[@class='well well-sm']/div/div/*[@class='row']/div/div[@class='well well-sm']"
  );
  for (var div in divs) {
    var select = getElementsByXPath(
      "div/div/*[@class='row']/div[@data-schemapath[starts-with(., 'root.')]]/div/select[@name[contains(., '[tag]')]]",
      divs[div]
    );
    try {
      var selectedOption = select[0].options[select[0].selectedIndex].label;
    } catch (err) {} // some of the values doesn't have tag field

    if (selectedOption != "not use") {
      usedTags.push(selectedOption);
    }
  }

  // update the tag field with the free tags available
  var divs = getElementsByXPath(
    "//*[@id='editor_holder']/div/div[@class='well well-sm']/div/div/*[@class='row']/div/div[@class='well well-sm']"
  );
  for (var div in divs) {
    var select = getElementsByXPath(
      "div/div/*[@class='row']/div[@data-schemapath[starts-with(., 'root.')]]/div/select[@name[contains(., '[tag]')]]",
      divs[div]
    );
    if (select.length > 0) {
      // if we found the 'tag' select
      var selectedOption = select[0].options[select[0].selectedIndex].label;
      try {
        for (var tag in usedTags) {
          if (select != undefined && selectedOption != usedTags[tag]) {
            disableFromSelectByValue(select, usedTags[tag]);
          }
        }
      } catch (err) {} // some of the values doesn't have tag field
    }
  }
}

function checkDivColor() {
  var divs = getElementsByXPath(
    "//*[@id='editor_holder']/div/div[@class='well well-sm']/div/div/*[@class='row']/div/div[@class='well well-sm']"
  );
  for (var div in divs) {
    var select = getElementsByXPath(
      "div/div/*[@class='row']/div[@data-schemapath[starts-with(., 'root.')]]/div/select[@name[contains(., '[tag]')]]",
      divs[div]
    );
    try {
      var selectedOption = select[0].options[select[0].selectedIndex].label;
    } catch (err) {} // some of the values doesn't have tag field

    if (selectedOption == "not use") {
      divs[div].style.backgroundColor = "#ffdddd";
      var nodes = divs[div].getElementsByTagName("*");
      for (var i = 0; i < nodes.length; i++) {
        var nodeName = nodes[i].name;
        if (typeof nodeName !== "undefined" && !nodeName.includes("tag")) {
          nodes[i].disabled = true;
        }
      }
    } else {
      divs[div].style.backgroundColor = "#ddfae2";
      var nodes = divs[div].getElementsByTagName("*");
      for (var i = 0; i < nodes.length; i++) {
        nodes[i].disabled = false;
      }
    }
  }
}

function checkUnitValues() {

  var formulas =
  "contains(., '[an') and contains(., '[formula]')";

  var tempUnits = ["celsius", "fahrenheit"];
  var pressureUnits = ["psi", "bar"];
  var otherUnits = ["per cent"];

  var divs = getElementsByXPath(
    "//*[@id='editor_holder']/div/div[@class='well well-sm']/div/div/*[@class='row']/div/div[@class='well well-sm']"
  );

  for (var div in divs) {

    var formula = getElementsByXPath(
      "div/div/*[@class='row']/div[@data-schemapath[starts-with(., 'root.')]]/div/select[@name["+formulas+"]]",
      divs[div]
    );
    if (formula.length > 0) {
        var selectedFormula = formula[0].options[formula[0].selectedIndex].value;
        var unitsSelect = getElementsByXPath("div/div/*[@class='row']/div[@data-schemapath[starts-with(., 'root.')]]/div/select[@name[contains(., '[unit]')]]", divs[div]);

        if (selectedFormula == "vdo_323_057"){
            var op = unitsSelect[0].getElementsByTagName("option");
            for (var i = 0; i < op.length; i++) {
                if (tempUnits.includes(op[i].value)){
                    op[i].disabled = false;
                    unitsSelect[0].selectedIndex = i;
                }
                else{
                    op[i].disabled = true;
                }
            }
        }

        else if (selectedFormula == "autometer_2246"){
            var op = unitsSelect[0].getElementsByTagName("option");
            for (var i = 0; i < op.length; i++) {
                if (pressureUnits.includes(op[i].value)){
                    op[i].disabled = false;
                    unitsSelect[0].selectedIndex = i;
                }
                else{
                    op[i].disabled = true;
                }
            }
        }

        else if (selectedFormula == "aem_30_2012"){
            var op = unitsSelect[0].getElementsByTagName("option");
            for (var i = 0; i < op.length; i++) {
                if (tempUnits.includes(op[i].value)){
                    op[i].disabled = false;
                    unitsSelect[0].selectedIndex = i;
                }
                else{
                    op[i].disabled = true;
                }
            }
        }

        else if (selectedFormula == "ebay_150_psi"){
            var op = unitsSelect[0].getElementsByTagName("option");
            for (var i = 0; i < op.length; i++) {
                if (pressureUnits.includes(op[i].value)){
                    op[i].disabled = false;
                    unitsSelect[0].selectedIndex = i;
                }
                else{
                    op[i].disabled = true;
                }
            }
        }

        else if (selectedFormula == "bosch_0280130039_0280130026"){
            var op = unitsSelect[0].getElementsByTagName("option");
            for (var i = 0; i < op.length; i++) {
                if (tempUnits.includes(op[i].value)){
                    op[i].disabled = false;
                    unitsSelect[0].selectedIndex = i;
                }
                else{
                    op[i].disabled = true;
                }
            }
        }

        else {
            var op = unitsSelect[0].getElementsByTagName("option");
            for (var i = 0; i < op.length; i++) {
                if (otherUnits.includes(op[i].value)){
                    op[i].disabled = false;
                    unitsSelect[0].selectedIndex = i;
                }
                else{
                    op[i].disabled = true;
                }
            }
        }
    }



  }


}

function updateFields() {
  checkDivColor();
  checkTagValues();
  checkUnitValues();
}

function download() {
  try {
    var dataStr =
      "data:text/json;charset=utf-8," +
      encodeURIComponent(JSON.stringify(editor.getValue(), null, 2));
    var dlAnchorElem = document.getElementById("downloadAnchorElem");
    dlAnchorElem.setAttribute("href", dataStr);
    dlAnchorElem.setAttribute("download", "setup.json");
    dlAnchorElem.click();
  } catch (e) {
    alert("sorry, an error occurred\n" + e.message);
  }
}

var webSocketUrl =
  "ws://" + (window.location.hostname || "127.0.0.1") + ":8080/ws";

function save() {
  var c = new autobahn.Connection({ url: webSocketUrl, realm: "realm1" });

  c.onopen = function(session) {
    session.call("save", [editor.getValue()]).then(
      function(setup) {
        schema["startval"] = setup;
        alert("setup saved");
      },
      function(e) {
        alert("sorry, an error occurred\n" + e.message);
      }
    );
  };
  c.open();
}

function reset() {
  var c = new autobahn.Connection({ url: webSocketUrl, realm: "realm1" });

  c.onopen = function(session) {
    session.call("reset").then(
      function(setup) {
        alert("setup reseted");
      },
      function(e) {
        alert("sorry, an error occurred\n" + e.message);
      }
    );
  };
  c.open();
}

try {
  var autobahn = require("autobahn");
} catch (e) {
  // when running in browser, AutobahnJS will
  // be included without a module system
}

var connection = new autobahn.Connection({
  url: webSocketUrl,
  realm: "realm1"
});

connection.onopen = function(session) {
  session.call("setup").then(function(setup) {
    schema["startval"] = setup;
    editor = new JSONEditor(document.getElementById("editor_holder"), schema);
    editor.on("change", updateFields); // for every change in the fields, trigger this function
    disableField(
      "//*[@id='editor_holder']/div/div[2]/div/div/div[1]/div/div[1]/input"
    ); // disable version field
  });
};

connection.open();
var editor;
