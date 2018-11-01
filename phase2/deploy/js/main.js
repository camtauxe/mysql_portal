// Selections for components
tableSelect     = d3.select('#tableselect');
table           = d3.select('#table');
fileSelect      = d3.select('#fileselect');
singleOption    = d3.select('#singleoption');
bulkOption      = d3.select('#bulkoption');
uploadButton    = d3.select('#uploadbutton');
clearButton     = d3.select('#clearbutton');
query           = d3.select('#query');
queryButton     = d3.select('#querybutton');
queryReadout    = d3.select('#queryreadout');

// Get list of tables from the database and populate
// the table select with the results
setGlobalEnabled(false);
fetch("/tables.py").then(function(response) {
    if (response.ok)
        return response.json();
    responseError("Unable to fetch table list!", response);
}).then(function(json) {
    tableSelect.selectAll('option')
        .data(json).enter()
        .append('option')
            .attr('value',function(d){return d;})
            .text(function(d){return d;});
    setGlobalEnabled(true);
    fetchAllData();
});

/**
 * Execute the query written in the query text field
 * and populate the table with the results
 */
function doQuery() {
    setGlobalEnabled(false)
    var queryText = query.node().value;
    if (queryText == "") {
        window.alert("You must enter a query!");
        setGlobalEnabled(true);
        return;
    }
    fetch("query.py?q="+encodeURIComponent(queryText)).then(function(response) {
        if (response.ok)
            return response.json();
        responseError("Unable to execute query!", response);
        setGlobalEnabled(true);
    }).then(function(json) {
        columns = json['columns'];
        data = [columns].concat(json['data']);
        rows = table.selectAll('tr').data(data);
        rows.exit().remove();
        rows.enter().append('tr')
            .merge(rows)
            .each(function(d) {
                cells = d3.select(this).selectAll('td').data(d);
                cells.exit().remove();
                cells.enter().append('td')
                    .merge(cells)
                    .text(function(k){ return k;});
            });
        queryReadout.text(json['rows']+" results in "+json['time']+" seconds.")
        if (json['rows'] > data.length-1)
            queryReadout.text(queryReadout.text()+" (showing first "+(data.length-1)+" rows)");
        setGlobalEnabled(true);
    });
}

/**
 * Populate the table with all of the data in the currently
 * selected table
 */
function fetchAllData() {
    var tableName = tableSelect.node().value;
    query.node().value = "SELECT * FROM " + tableName;
    doQuery();
}

/**
 * Upload the selected file from the fileSelect to the selected
 * table in the selected mode.
 */
function upload() {
    setGlobalEnabled(false);
    var fileList = fileSelect.node().files;
    var tableName = tableSelect.node().value;
    if (fileList.length == 0) {
        window.alert("You must select a file first!");
        setGlobalEnabled(true);
        return;
    }
    var type = bulkOption.node().checked ? bulkOption.node().value : singleOption.node().value
    var file = fileList[0];
    var data = new FormData();
    data.append('file',file)

    fetch("upload.py?type="+type+"&t="+tableName, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: file
    }).then(function(response) {
        if (response.ok)
            return response.json();
        responseError("Error with uploaded data!", response);
    }).then(function(json) {
        fetchAllData();
        window.alert("Insertion completed in "+json.time+" seconds!");
    });
}

/**
 * Clear the currently selected table
 */
function clearTable() {
    setGlobalEnabled(false);
    var tableName = tableSelect.node().value;

    fetch("clear.py?t="+tableName, {
        method: "POST"
    }).then(function(response) {
        if (response.ok) {
            fetchAllData();
            return;
        }
        responseError("Error clearing table!", response);
        setGlobalEnabled(true);
    });
}

/**
 * Enable or disable all the controls on the page.
 * It's a good idea to disable all the controls while
 * waiting on the response to a request to avoid creating
 * confounding requests in the meantime.
 */
function setGlobalEnabled(enabled) {
    tableSelect.node().disabled     = !enabled;
    clearButton.node().disabled     = !enabled;
    uploadButton.node().disabled    = !enabled;
    queryButton.node().disabled     = !enabled;
}

/**
 * Display an error message detailing the given
 * not-ok HTTP response.
 * An alert will be displayed with the given message and
 * then showing the status code and body of the response.
 */
function responseError(message, response) {
    response.text().then(function(text) {
        window.alert(
            message + "\n" +
            "Server said:\n" +
            response.status + ": " + response.statusText + "\n" +
            text
        );
    })
}