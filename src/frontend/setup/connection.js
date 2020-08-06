// utils
var formulas = "contains(., '[an') and contains(., '[formula]')";
var formulaVsUnits = {
  vdo_323_057: ["celsius", "fahrenheit"],
  autometer_2246: ["psi", "mbar", "bar"],
  aem_30_2012: ["celsius", "fahrenheit"],
  ebay_150_psi: ["psi", "mbar", "bar"],
  bosch_0280130039_0280130026: ["celsius", "fahrenheit"]
};
var otherUnits = ["per cent"];
var enabledBackgroundColorDiv = "#ddfae2";
var disabledBackgroundColorDiv = "#ffdddd";

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

function disableFromSelectByValue(select, value) {
  for (var option in select[0].options) {
    if (select[0].options[option].label == value) {
      select[0].options[option].disabled = true;
      break;
    }
  }
}

function enableAllSelectOptions(select) {
  for (var option in select[0].options) {
    select[0].options[option].disabled = false;
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

function checkTagValues() {
  var usedTags = [];
  var rowsPerValue = getElementsByXPath(
    "//*[@id='editor_holder']/div/div[@class='card card-body mb-3 bg-light']/div/div/*[@class='row']"
  );

  // fill list of used tags
  for (var row in rowsPerValue) {
    var divs = getElementsByXPath("div", rowsPerValue[row]);
    for (var div in divs) {
      var valueDiv = getElementsByXPath(
        "div[@class='card card-body mb-3 bg-light']",
        divs[div]
      );
      var rowContainingTag = getElementsByXPath(
        "div/div/*[@class='row']/div[@data-schemapath[contains(., 'tag')]]",
        valueDiv[0]
      );
      for (var row in rowContainingTag) {
        var select = getElementsByXPath("div/select", rowContainingTag[row]);
        if (select.length <= 0) {
          // if no select found just skip
          break;
        }
        var selectedOption = select[0].options[select[0].selectedIndex].label;
        if (selectedOption != "not use") {
          usedTags.push(selectedOption);
        }
      }
    }
  }

  // update the tag field with the free tags available
  for (var row in rowsPerValue) {
    var divs = getElementsByXPath("div", rowsPerValue[row]);
    for (var div in divs) {
      var valueDiv = getElementsByXPath(
        "div[@class='card card-body mb-3 bg-light']",
        divs[div]
      );
      var rowContainingTag = getElementsByXPath(
        "div/div/*[@class='row']/div[@data-schemapath[contains(., 'tag')]]",
        valueDiv[0]
      );
      for (var row in rowContainingTag) {
        var select = getElementsByXPath("div/select", rowContainingTag[row]);
        if (select.length <= 0) {
          // if no select found just skip
          break;
        }
        var selectedOption = select[0].options[select[0].selectedIndex].label;
        enableAllSelectOptions(select);
        for (var tag in usedTags) {
          if (select != undefined && selectedOption != usedTags[tag]) {
            disableFromSelectByValue(select, usedTags[tag]);
          }
        }
      }
    }
  }
}

function checkDivColor() {
  var rowsPerValue = getElementsByXPath(
    "//*[@id='editor_holder']/div/div[@class='card card-body mb-3 bg-light']/div/div/*[@class='row']"
  );

  for (var row in rowsPerValue) {
    var divs = getElementsByXPath("div", rowsPerValue[row]);
    for (var div in divs) {
      var valueDiv = getElementsByXPath(
        "div[@class='card card-body mb-3 bg-light']",
        divs[div]
      );

      // starting by putting all the divs in green
      if (valueDiv[0] !== undefined) {
        valueDiv[0].style.setProperty(
          "background-color",
          enabledBackgroundColorDiv,
          "important"
        );
      }
      var rowContainingTag = getElementsByXPath(
        "div/div/*[@class='row']/div[@data-schemapath[contains(., 'tag')]]",
        valueDiv[0]
      );
      for (var row in rowContainingTag) {
        var select = getElementsByXPath("div/select", rowContainingTag[row]);
        if (select.length <= 0) {
          // if no select found just skip
          break;
        }
        var selectedOption = select[0].options[select[0].selectedIndex].label;

        // paint the div and enable or disable the boxes
        if (selectedOption == "not use") {
          valueDiv[0].style.setProperty(
            "background-color",
            disabledBackgroundColorDiv,
            "important"
          );
          var nodes = valueDiv[0].getElementsByTagName("*");
          for (var i = 0; i < nodes.length; i++) {
            var nodeName = nodes[i].name;
            if (typeof nodeName !== "undefined" && !nodeName.includes("tag")) {
              nodes[i].disabled = true;
            }
          }
        } else {
          valueDiv[0].style.setProperty(
            "background-color",
            enabledBackgroundColorDiv,
            "important"
          );
          var nodes = divs[div].getElementsByTagName("*");
          for (var i = 0; i < nodes.length; i++) {
            nodes[i].disabled = false;
          }
        }
      }
    }
  }
}

function checkUnitValues() {
  var rowsPerValue = getElementsByXPath(
    "//*[@id='editor_holder']/div/div[@class='card card-body mb-3 bg-light']/div/div/*[@class='row']"
  );

  for (var row in rowsPerValue) {
    var divs = getElementsByXPath("div", rowsPerValue[row]);
    for (var div in divs) {
      var valueDiv = getElementsByXPath(
        "div[@class='card card-body mb-3 bg-light']",
        divs[div]
      );
      var rowContainingFormula = getElementsByXPath(
        "div/div/*[@class='row']/div[@data-schemapath[contains(., 'formula')]]",
        valueDiv[0]
      );
      for (var row in rowContainingFormula) {
        var select = getElementsByXPath(
          "div/select",
          rowContainingFormula[row]
        );
        var selectedFormula = select[0].options[select[0].selectedIndex].label;
        var rowContainingUnit = getElementsByXPath(
          "div/div/*[@class='row']/div[@data-schemapath[contains(., 'unit')]]",
          valueDiv[0]
        );
        select = getElementsByXPath("div/select", rowContainingUnit[row]);

        // if the formula is a recognized one
        if (selectedFormula in formulaVsUnits) {
          enforceAllowedUnits(select, formulaVsUnits[selectedFormula]);
        } else {
          enforceAllowedUnits(select, otherUnits);
        }

        // force json editor library to notice that we did nasty things in the unit select
        var selectNode = document.getElementById(select[0].name);
        selectNode.dispatchEvent(new Event("change"));
      }
    }
  }
}

function updateFields() {
  checkDivColor();
  checkTagValues();
  checkUnitValues();
}

// file uploader shit
function clickFileUploader() {
  document.getElementById("file_id").click();
}

function onFileUploaderChange(event) {
  var reader = new FileReader();
  reader.onload = onReaderLoad;
  reader.readAsText(event.target.files[0]);
}

function onReaderLoad(event) {
  var uploadedJson = JSON.parse(event.target.result);
  ws.send(JSON.stringify({ action: "save", data: uploadedJson }));
}

// buttons related functions
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

function save() {
  ws.send(JSON.stringify({ action: "save", data: editor.getValue() }));
}

function reset() {
  ws.send(JSON.stringify({ action: "reset" }));
}

var editor;
var ws = new WebSocket(
  "ws://" + (window.location.hostname || "127.0.0.1") + ":5678/"
);
document
  .getElementById("file_id")
  .addEventListener("change", onFileUploaderChange);

ws.onmessage = function(event) {
  var data = JSON.parse(event.data);
  var keys = Object.keys(data);

  // if the setup has not been received
  if (schema["startval"] === undefined) {
    if (keys[0] == "setup") {
      schema["startval"] = data["setup"];
      editor = new JSONEditor(document.getElementById("editor_holder"), schema);
      editor.on("change", updateFields); // for every change in the fields, trigger this function
    }
  } else {
    if (keys.indexOf("action") > -1) {
      // it's an action?
      if (data["action"] == "alert") {
        alert(data["message"]);
      }
    }
  }
};

// asks for the setup as soon as possible
ws.onopen = function(e) {
  ws.send(JSON.stringify({ action: "setup" }));
};
// in case something blows up or connection gets close, keep trying
ws.onerror = function(e) {
  location.reload();
};
ws.onclose = function(e) {
  location.reload();
};
