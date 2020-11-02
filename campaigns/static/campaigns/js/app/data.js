

function createCanvas(identifier){
    var hmtl = 
    `
    <div class="col-12 col-lg-12" id="divChart${identifier}">
        <canvas id="canvas${identifier}"></canvas>
    </div>
    `;
    $('#answerChartContainer').append(html);
}

function createConfig(question){
    var answers = question.answers;
    var labels = [];
    var colors = [];
    var data = [];
    var index = 0;

    for(answer of answers){
        labels.append(answer.text);
        colors.append(getColor(index));
        data.append(answer.count);
    }

    var config = {
        type: 'pie',
        data: {
            datasets: [{
                data: data,
                backgroundColor: colors,
                label: question.text
            }],
            labels: labels
        }
    }

    return config;
}

function getColor(index){
    var choosed = index % 5;
    switch(choosed){
        case 0:
            return window.chartColors.red;
        case 1:
            return window.chartColors.orange;
        case 2:
            return window.chartColors.yellow;
        case 3:
            return window.chartColors.green;
        case 4:
            return window.chartColors.blue;
    }
}

$( document ).ready(function() {

    $('#downloadButton').click(function(){
        var start_date = $('#fechaInicioInput').val();
        var end_date = $('#fechaFinInput').val();
        var url = download_poll_answers_url;
        url = url.replace("abc", start_date);
        url = url.replace("def", end_date);
        window.location.href = url;
    });
});

/*
window.onload = function() {
    var ctx = document.getElementById('chart-area').getContext('2d');
    window.myPie = new Chart(ctx, config);
};

document.getElementById('randomizeData').addEventListener('click', function() {
    config.data.datasets.forEach(function(dataset) {
        dataset.data = dataset.data.map(function() {
            return randomScalingFactor();
        });
    });

    window.myPie.update();
});

var colorNames = Object.keys(window.chartColors);
document.getElementById('addDataset').addEventListener('click', function() {
    var newDataset = {
        backgroundColor: [],
        data: [],
        label: 'New dataset ' + config.data.datasets.length,
    };

    for (var index = 0; index < config.data.labels.length; ++index) {
        newDataset.data.push(randomScalingFactor());

        var colorName = colorNames[index % colorNames.length];
        var newColor = window.chartColors[colorName];
        newDataset.backgroundColor.push(newColor);
    }

    config.data.datasets.push(newDataset);
    window.myPie.update();
});

document.getElementById('removeDataset').addEventListener('click', function() {
    config.data.datasets.splice(0, 1);
    window.myPie.update();
});*/