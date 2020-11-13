var urls = {};
var standard = {};

$('#agentInput').selectpicker(
    {
        "liveSearch": true
    }
);

function failPrepare(){
    var start_date = $('#fechaInicioInput').val();
    var end_date = $('#fechaFinInput').val();
    if(start_date == "") agent = today_date();
    if(end_date == "") agent = today_date();

    var data = {
        'start_date': start_date,
        'end_date': end_date
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
    standard.makePetition(data, 'fail_prepare_url', ajaxFunctions);
}

function today_date(){
    var today = new Date();
    var dd = today.getDate();

    var mm = today.getMonth()+1; 
    var yyyy = today.getFullYear();
    if(dd<10) 
    {
        dd='0'+dd;
    } 

    if(mm<10) 
    {
        mm='0'+mm;
    } 

    return yyyy + "-" + mm + "-" + dd;
}

$( document ).ready(function() {

    urls = {
        'fail_prepare_url': {'url' : fail_prepare_url, 'method':'POST'},
    }
    standard = new StandardCrud(urls);


    FormFunctions.setAjaxLoadPicker(
        '#agentInput', pircker_search_agent_url, FormFunctions.updatePicker, "Ningun agente"
    );

    FormFunctions.ajaxLoadPicker(
        '#agentInput', pircker_search_agent_url, FormFunctions.updatePicker, "", "Ningun agente"
    );

    $('#downloadButton').click(function(){
        var start_date = $('#fechaInicioInput').val();
        var end_date = $('#fechaFinInput').val();
        var agent = $('#agentInput').val();
        var url = download_poll_answers_url;
        var today = new Date();
        if(start_date == "") start_date = today_date();
        if(end_date == "") end_date = today_date();
        if(agent == "") agent = "0";
        url = url.replace("abc", start_date);
        url = url.replace("def", end_date);
        url = url.replace("0", agent);
        window.location.href = url;
    });

    $('#downloadFailsButton').click(function(){
        var start_date = $('#fechaInicioInput').val();
        var end_date = $('#fechaFinInput').val();
        var url = download_fails_url;
        var today = new Date();
        if(start_date == "") start_date = today_date();
        if(end_date == "") end_date = today_date();
        url = url.replace("abc", start_date);
        url = url.replace("def", end_date);
        window.location.href = url;
    });

    $('#reCallButton').click(function(){
        failPrepare();
    });
    

});