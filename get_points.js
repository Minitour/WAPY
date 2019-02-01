function loadJSON(filelocation,callback) {   

    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', filelocation, false); // Replace 'my_data' with the path to your file
    xobj.onreadystatechange = function () {
        if (xobj.readyState == 4 && xobj.status == "200") {
            //console.log(xobj.response);
            // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
            //console.log("bbb" + xobj.response);
            callback(xobj.response);
        }
    };
    xobj.send();  
}

function init() {
    var location = "./points.json";
    var returned = null;
    loadJSON(location, function(json) {
        var returned_json = JSON.parse(json);
        returned = JSON.stringify(returned_json.results);
        //console.log("vvv" + JSON.stringify(returned_json));
    });
    
    //console.log("iii:" + returned);
    return returned;
}

var returned_json = init();
//console.log(returned_json);
// var points_json = init();
//console.log(points_json);


// var points_json = {"results": [
//     {"x": 257.0, "y": 274.0, "value": 98, "radius": "20"},
//     {"x": 363.0, "y": 267.0, "value": 5, "radius": "20"},
//     {"x": 272.0, "y": 269.0, "value": 1, "radius": "20"},
//     {"x": 70.0, "y": 266.0, "value": 2, "radius": "20"},
//     {"x": 39.0, "y": 265.0, "value": 1, "radius": "20"},
//     {"x": 219.0, "y": 266.0, "value": 1, "radius": "20"},
//     {"x": 539.0, "y": 265.0, "value": 1, "radius": "20"},
//     {"x": 74.0, "y": 271.0, "value": 1, "radius": "20"}
//   ]}
