var hoursChart = {};
var hoursChartCreated = false;
function createDataSet(strlabel, color, data){
    var set = {
        label: strlabel,
        borderColor: color,
        borderWidth: 4,
        data: data,
        fill:false
    };
    return set;
}

function createDataHorasCallEntry(call_entry_per_hour){
    var calls_per_hour = call_entry_per_hour.calls_per_hour;
    var calls_abandonadas = call_entry_per_hour.calls_abandonadas;
    var call_terminadas = call_entry_per_hour.call_terminadas;

    data_set_total = createDataSet('Total', window.chartColors.yellow, calls_per_hour);
    data_set_abandonadas = createDataSet('Abandonadas', window.chartColors.red, calls_abandonadas);
    data_set_terminadas = createDataSet('Terminadas', window.chartColors.green, call_terminadas);

    return [data_set_total, data_set_abandonadas, data_set_terminadas];
}

function createHoursChart(data){
    var canvas = document.getElementById('canvasBarras');
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    hoursChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            legend: {
                position: 'top',
                display : true,
                labels: {
                    fontSize: 12
                }
            },
            title: {
                display: true,
                text: 'Resumen de llamadas',
                fontSize: 16
            },
            /*
            scales: {
                xAxes: [{
                    gridLines: {
                        color: "rgba(0, 0, 0, 0)",
                    }
                }],
                yAxes: [{
                    gridLines: {
                        color: "rgba(0, 0, 0, 0)",
                    }   
                }]
            },*/
            animation: {
                duration: 0
            },
            onAnimationComplete: function () {
                var ctx = this.chart.ctx;
                ctx.font = this.scale.font;
                ctx.fillStyle = this.scale.textColor;
                ctx.textAlign = "center";
                ctx.textBaseline = "bottom";

                this.datasets.forEach(function (dataset) {
                    dataset.bars.forEach(function (bar) {
                        ctx.fillText(bar.value, bar.x, bar.y - 5);
                    });
                })
            }
        }
    });
}

function updateHoursChart(data){
    hoursChart.data = data;
    hoursChart.update();
}

function drawHoursChart(call_entry_per_hour){
    var x = [1,2,3];
    console.log(x);
    console.log(call_entry_per_hour);
    var datasets = createDataHorasCallEntry(call_entry_per_hour);
    var data = {
        labels: ['00', '01', '02', '03', '04','05','06','07','08','09','10','11',
            '12','13','14','15','16','17','18','19','20','21','22','23'],
        datasets: datasets
    }

    if(hoursChartCreated){
        updateHoursChart(data);
    }
    else{
        createHoursChart(data);
    }
}
