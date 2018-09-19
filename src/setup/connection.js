function getElementsByXPath(xpath, parent) {
  let results = [];
  let query = document.evaluate(xpath,
      parent || document,
      null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
  for (let i=0, length=query.snapshotLength; i<length; ++i) {
    results.push(query.snapshotItem(i));
  }
  return results;
}

function disableField(xpath) {
    getElementsByXPath(xpath)[0].disabled=true;
}

function updateFields() {
    var divs = getElementsByXPath("//*[@id='editor_holder']/div/div[@class='well well-sm']/div/div/*[@class='row']/div/div[@class='well well-sm']");
    for (var i in divs){
        var select = getElementsByXPath("div/div/*[@class='row']/div[@data-schemapath[starts-with(., 'root.')]]/div/select[@name[contains(., '[tag]')]]", divs[i]);
        try {
            var selectedOption = select[0].options[select[0].selectedIndex].label;
        } catch(err) {} // some of the values doesn't have tag field

        if (selectedOption == 'not use'){
            divs[i].style.backgroundColor = "#ffdddd";
            var nodes = divs[i].getElementsByTagName('*');
            for (var i = 0; i < nodes.length; i++){
                var nodeName = nodes[i].name;
                if (typeof nodeName !== "undefined" && !nodeName.includes('tag')){
                    nodes[i].disabled = true;
                }
            }
        }
        else {
            divs[i].style.backgroundColor = "#ddfae2";
            var nodes = divs[i].getElementsByTagName('*');
            for (var i = 0; i < nodes.length; i++){
                nodes[i].disabled = false;
            }
        }
    }
}

function download(){
    try {
        var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(editor.getValue(), null, 2));
        var dlAnchorElem = document.getElementById('downloadAnchorElem');
        dlAnchorElem.setAttribute("href", dataStr);
        dlAnchorElem.setAttribute("download", "setup.json");
        dlAnchorElem.click();
    } catch (e) {
        alert("sorry, an error occurred\n" + e.message);
    }
}

function save(){
    var c = new autobahn.Connection({url: 'ws://' + window.location.hostname + ':8080/ws', realm: 'realm1'});

    c.onopen = function (session) {
        session.call("save", [editor.getValue()]).then(
            function (setup) {
                schema['startval'] = setup;
                alert("setup saved");
            },
            function (e) {
                alert("sorry, an error occurred\n" + e.message);
            }
        );
    };
    c.open();
}

try {
   var autobahn = require('autobahn');
} catch (e) {
   // when running in browser, AutobahnJS will
   // be included without a module system
}

var connection = new autobahn.Connection({
   url: 'ws://' + window.location.hostname + ':8080/ws',
   realm: 'realm1'}
);

connection.onopen = function (session) {
    session.call("setup").then(
        function (setup) {
            schema['startval'] = setup;
            editor = new JSONEditor(document.getElementById('editor_holder'), schema);
            editor.on('change',updateFields); // for every change in the fields, trigger this function
            disableField("//*[@id='editor_holder']/div/div[2]/div/div/div[1]/div/div[1]/input"); // disable version field
        }
    );
};

connection.open();
var editor;
