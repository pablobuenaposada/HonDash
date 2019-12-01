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

function enforceAllowedUnits(unitsSelect, allowedUnits) {
  var option = unitsSelect[0].getElementsByTagName("option");
  var allowedUnitIndex = -1;
  for (var i = 0; i < option.length; i++) {
    if (allowedUnits.includes(option[i].value)) {
      option[i].disabled = false;
      allowedUnitIndex = i;
    } else {
      option[i].disabled = true;
    }
  }

  // if the selected unit is not allowed, move it to a new allowed one
  if (!allowedUnits.includes(option[unitsSelect[0].selectedIndex].value)) {
    unitsSelect[0].selectedIndex = allowedUnitIndex;
  }
}

var formulas = "contains(., '[an') and contains(., '[formula]')";
var formulaVsUnits = {
  vdo_323_057: ["celsius", "fahrenheit"],
  autometer_2246: ["psi", "bar"],
  aem_30_2012: ["celsius", "fahrenheit"],
  ebay_150_psi: ["psi", "bar"],
  bosch_0280130039_0280130026: ["celsius", "fahrenheit"]
};
var otherUnits = ["per cent"];

function checkUnitValues() {
  var divs = getElementsByXPath(
    "//*[@id='editor_holder']/div/div[@class='well well-sm']/div/div/*[@class='row']/div/div[@class='well well-sm']"
  );

  for (var div in divs) {
    var formula = getElementsByXPath(
      "div/div/*[@class='row']/div[@data-schemapath[starts-with(., 'root.')]]/div/select[@name[" +
        formulas +
        "]]",
      divs[div]
    );
    if (formula.length > 0) {
      var selectedFormula = formula[0].options[formula[0].selectedIndex].value;
      var unitsSelect = getElementsByXPath(
        "div/div/*[@class='row']/div[@data-schemapath[starts-with(., 'root.')]]/div/select[@name[contains(., '[unit]')]]",
        divs[div]
      );

      // if the formula is a recognized one
      if (selectedFormula in formulaVsUnits) {
        enforceAllowedUnits(unitsSelect, formulaVsUnits[selectedFormula]);
      } else {
        enforceAllowedUnits(unitsSelect, otherUnits);
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
