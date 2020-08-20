var hoursChart = {};
var hoursChartOut = {};
var hoursChartCreated = false;
var hoursChartOutCreated = false;
function createDataSet(strlabel, colorrgba, data){
    var set = {
        label: strlabel,
        borderColor: colorrgba,
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

function createDataHorasCalls(calls_out_per_hour){
    var calls_per_hour = calls_out_per_hour.calls_per_hour;
    var calls_abandonadas = calls_out_per_hour.calls_abandonadas;
    var calls_terminadas = calls_out_per_hour.calls_terminadas;

    data_set_total = createDataSet('Total', window.chartColors.yellow, calls_per_hour);
    data_set_abandonadas = createDataSet('Fallidas', window.chartColors.red, calls_abandonadas);
    data_set_terminadas = createDataSet('Terminadas', window.chartColors.green, calls_terminadas);

    return [data_set_total, data_set_abandonadas, data_set_terminadas];
}


function createHoursChart(data, canvas, type){
    var canvas = document.getElementById(canvas);
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    

    var chart = new Chart(ctx, {
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

    if(type == 'out'){
        hoursChartOut = chart;
        hoursChartOutCreated = true;
    }
    else{
        hoursChart = chart;
        hoursChartCreated = true;
    }

    
}

function updateHoursChart(data, chart){
    chart.data = data;
    chart.options.animation.duration = 0;
    chart.update();
}

function drawHoursChart(call_entry_per_hour){
    var x = [1,2,3];
    var datasets = createDataHorasCallEntry(call_entry_per_hour);
    var data = {
        labels: ['00', '01', '02', '03', '04','05','06','07','08','09','10','11',
            '12','13','14','15','16','17','18','19','20','21','22','23'],
        datasets: datasets
    }
    if(hoursChartCreated){
        updateHoursChart(data, hoursChart);
    }
    else{
        createHoursChart(data, 'canvasBarras', 'entry');
    }
}

function drawHoursChartOut(call_entry_per_hour){
    var x = [1,2,3];
    var datasets = createDataHorasCalls(call_entry_per_hour);
    var data = {
        labels: ['00', '01', '02', '03', '04','05','06','07','08','09','10','11',
            '12','13','14','15','16','17','18','19','20','21','22','23'],
        datasets: datasets
    }
    if(hoursChartOutCreated){
        updateHoursChart(data, hoursChartOut);
    }
    else{
        createHoursChart(data, 'canvasBarrasSalientes', 'out');
    }
}
