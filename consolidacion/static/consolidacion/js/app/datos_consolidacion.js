
$('#agentInput').selectpicker(
    {
        "liveSearch": true
    }
);

$( document ).ready(function() {
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
        if(start_date == "") agent = today();
        if(end_date == "") agent = today();
        if(agent == "") agent = "0";
        url = url.replace("abc", start_date);
        url = url.replace("def", end_date);
        url = url.replace("0", agent);
        window.location.href = url;
    });

});