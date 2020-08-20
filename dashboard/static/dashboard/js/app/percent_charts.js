var tmoChart = {};
var effectivenessChart = {};
var serviceLevelChart = {};
var tmoChartCreated = false;
var effectivenessChartCreated = false;
var serviceLevelChartCreated = false;

function createDataDoughnut(percent, labels){
    let other = Math.ceil(100 - percent);
    let level = Math.floor(percent);
    var colorrgba;
    if(percent < 80){
        colorrgba = window.chartColors.red;
    }
    else if(percent < 96){
        colorrgba = window.chartColors.yellow;
    }
    else{
        colorrgba = window.chartColors.green;
    }

    return {
        labels: labels,
        datasets: [{
            label: 'TMO',
            backgroundColor: color(colorrgba).alpha(0.8).rgbString(),
            borderColor: colorrgba,
            borderWidth: 1,
            data: [
                level,
                other,
            ],
            backgroundColor: [
                colorrgba,
                '#f8f9fc',
            ],
        }]
    };
}

function createDoughnutSemaphoreChart(data, canvas, title_text){
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    chart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            maintainAspectRatio: false,
            cutoutPercentage: 80,
            responsive: true,
            legend: {
                position: 'top',
                display : false,
            },
            title: {
                display: false,
                text: title_text,
                fontSize: 16,
                padding: 10,
                lineHeight: 1.2
            },
            tooltips: {
                callbacks: {
                    label: function(tooltipItem, data) {
                        var label = data['labels'][tooltipItem['index']];

                        if (label) {
                            label += ': ';
                        }
                        label += data['datasets'][0]['data'][tooltipItem['index']];
                        label += "%";
                        return label;
                    }
                }
            }
        }
    });
    return chart;
}

function updateDoughnutSemaphoreChart(data, chart){
    chart.data = data;
    chart.update({
        duration: 0,
    });
}

function drawTmoChart(tmo, segundos){
    var labels = [`TMO`, 'TMO Fallidas'];
    var data = createDataDoughnut(tmo, labels);
    $("#tmoLabel").html(`${Math.floor(tmo)}%`);
    if(tmoChartCreated){
        updateDoughnutSemaphoreChart(data, tmoChart);
    }
    else{
        var canvas = document.getElementById('canvasTmo');
        tmoChart = createDoughnutSemaphoreChart(data, canvas, 'TMO');
        tmoChartCreated = true;
    }
}

function drawEffectivenessChart(effectiveness){
    var labels = [`Efectividad`, 'No efectivas'];
    var data = createDataDoughnut(effectiveness, labels);
    $("#efectivenessLabel").html(`${Math.floor(effectiveness)}%`);
    if(effectivenessChartCreated){
        updateDoughnutSemaphoreChart(data, effectivenessChart);
    }
    else{
        var canvas = document.getElementById('canvasEffectiveness');
        effectivenessChart = createDoughnutSemaphoreChart(data, canvas, 'Efectividad');
        effectivenessChartCreated = true;
    }
}

function drawServiceLevelChart(serviceLevel, segundos){
    var labels = [`Nivel de servicio`, 'Perdidas'];
    var data = createDataDoughnut(serviceLevel, labels);
    $("#serviceLabel").html(`${Math.floor(serviceLevel)}%`);
    if(serviceLevelChartCreated){
        updateDoughnutSemaphoreChart(data, serviceLevelChart);
    }
    else{
        var canvas = document.getElementById('canvasServiceLevel');
        serviceLevelChart = createDoughnutSemaphoreChart(data, canvas, 'Nivel de servicio');
        serviceLevelChartCreated = true;
    }
}

