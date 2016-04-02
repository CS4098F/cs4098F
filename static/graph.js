var options;

function drawGraph() {
    
    options = $('#options').serialize();

    src = "https://chart.googleapis.com/chart?"+options
    $('#graph').attr("src", src);
}