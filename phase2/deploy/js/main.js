// Selections for components
tableSelect = d3.select('#tableselect');
table       = d3.select('#table');

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
 * Populate the table with all of the data in the currently
 * selected table
 */
function fetchAllData() {
    tableName = tableSelect.node().value;
    setGlobalEnabled(false);
    fetch("getall.py?t="+tableName).then(function(response) {
        if (response.ok)
            return response.json();
        responseError("Unable to fetch data!", response);
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
        setGlobalEnabled(true);
    })
}

/**
 * Enable or disable all the controls on the page.
 * It's a good idea to disable all the controls while
 * waiting on the response to a request to avoid creating
 * confounding requests in the meantime.
 */
function setGlobalEnabled(enabled) {
    tableSelect.node().disabled = !enabled;
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