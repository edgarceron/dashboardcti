var standard;

function createCanvas(identifier){
    var html = 
    `
    <div class="col-12 col-lg-6" id="divChart${identifier}">
        <canvas id="canvas${identifier}"></canvas>
    </div>
    `;
    $('#answerChartContainer').append(html);
    return `canvas${identifier}`;
}

function createConfig(question){
    var title_text = question.text;
    var answers = question.answers;
    var labels = [];
    var colors = [];
    var data = [];
    var index = 0;

    for(pk in answers){
        labels.push(answers[pk].text);
        colors.push(getColor(index));
        data.push(answers[pk].count);
        index++;
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
        },
        options: {
            title: {
                display: true,
                text: title_text,
                fontSize: 16,
                lineHeight: 1.2
            }
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

function getDataChart(){
    $('#answerChartContainer').empty();
    var data = {
        'id_campaign': id,
        'start_date': $('#fechaInicioInput').val(),
        'end_date': $('#fechaFinInput').val()
    };
    var ajaxFunctions = {
        'success': function(result){
            var questions = JSON.parse(result.questions);
            var canvas;
            var config;
            var ctx;
            var chart;
            for(pk in questions){
                canvas = createCanvas(pk);
                config = createConfig(questions[pk]);
                ctx = document.getElementById(canvas).getContext('2d');
                chart = new Chart(ctx, config);
            }
        },
        'error': function(result){

        }
    }
    standard.makePetition(data, 'data_chart_campaign_url', ajaxFunctions);
}

function prepareFails(){
    var start_date = $('#fechaInicioInput').val();
    var end_date = $('#fechaFinInput').val();
    if(start_date == "") agent = today();
    if(end_date == "") agent = today();

    var data = {
        'start_date': start_date,
        'end_date': end_date,
        'campaign': id,
    }

    var ajaxFunctions = {
        'success': function(result){
            var color;
            if(result.success) color = "success";
            else color = "danger";
            SoftNotification.show(result.message, color);
        },
        'error': function(result){
            SoftNotification.show("Ocurrio un error", "danger");
        }
    }
    standard.makePetition(data, 'fail_prepare_polls_url', ajaxFunctions);
}

$( document ).ready(function() {

    var urls = {
        'data_chart_campaign_url':{'url' : data_chart_campaign_url, 'method':'POST'},
        'fail_prepare_polls_url':{'url' : fail_prepare_polls_url, 'method':'POST'},
    }
    standard = new StandardCrud(urls);

    $('#downloadButton').click(function(){
        var start_date = $('#fechaInicioInput').val();
        var end_date = $('#fechaFinInput').val();
        var url = download_poll_answers_url;
        if(start_date == "") start_date = today();
        if(end_date == "") end_date = today();
        url = url.replace("abc", start_date);
        url = url.replace("def", end_date);
        window.location.href = url;
    });

    $('#downloadFailsButton').click(function(){
        var start_date = $('#fechaInicioInput').val();
        var end_date = $('#fechaFinInput').val();
        var url = download_fails_polls_url;
        if(start_date == "") start_date = today();
        if(end_date == "") end_date = today();
        url = url.replace("abc", start_date);
        url = url.replace("def", end_date);
        window.location.href = url;
    });

    $('#reloadCharts').click(function(){
        getDataChart();
    });

    getDataChart();
});