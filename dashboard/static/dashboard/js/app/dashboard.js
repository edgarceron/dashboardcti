var dashboardType = 1;

function getValues(){
    var data = {
        'id_agent': $('#agentInput').val(),
        'id_campaign': $('#campaignInput').val(),
        'start_date': $('#startDateInput').val(),
        'end_date': $('#endDateInput').val(),
    }
    return data;
}

function getData(){
    if(dashboardType == 1){
        getDataEntry();
    }
    else{
        getDataOut();
    }
}

function getDataOut(){
    standard.async = true;
    var ajaxFunctions = {
        'success': function(result){
            drawHoursChartOut(result.calls_out_per_hour);
            setStatsLabelsOut(result.calls_count);
            drawCompletionChart(result.completion_rate);
            drawSuccessChart(result.success_rate);
            setStatsOperations(
                result.consolidacion_count,
                result.polls_attended
            );
        },
        'error': standard.standardError,
        'complete': function(){
            setTimeout(function(){ 
                getData();
            }, 3000);
        }
    }

    standard.makePetition(getValues(), 'get_data_dashboard_out_url', ajaxFunctions);
}

function getDataEntry(){
    standard.async = true;
    var ajaxFunctions = {
        'success': function(result){
            drawHoursChart(result.call_entry_per_hour);
            drawTmoChart(result.tmo, result.seconds);
            drawEffectivenessChart(result.effectiveness);
            drawServiceLevelChart(result.service_level, result.seconds);
            setStatsLabels(result.call_entry_count);
            setStatsAgents(
                result.agents_logged,
                result.agents_in_break,
                result.agents_in_call
            );
            setStatsOperationsEntry(
                result.citas_count,
                result.polls_attended
            );
        },
        'error': standard.standardError,
        'complete': function(){
            setTimeout(function(){ 
                getData();
            }, 3000);
        }
    }

    standard.makePetition(getValues(), 'get_data_dashboard_url', ajaxFunctions);
}


$( document ).ready(function() {
    $('#informe').val(1);
    $('#dashboardEntry').collapse('show');
    $('#informe').change(function(){
        var seleccionado = $('#informe').val();
        if(seleccionado == 1){
            $('#dashboardEntry').collapse('show');
            $('#dashboardOut').collapse('hide');
            dashboardType = 1;
        }
        else{
            $('#dashboardEntry').collapse('hide');
            $('#dashboardOut').collapse('show');
            dashboardType = 2;
        }
    });

    $('#campaignInput').selectpicker(
        {
            "liveSearch": true
        }
    );

    FormFunctions.setAjaxLoadPicker(
        '#campaignInput', picker_search_campaign_url, 
        FormFunctions.updatePicker, "Todas las campañas"
    );
    FormFunctions.ajaxLoadPicker(
        '#campaignInput', picker_search_campaign_url, 
        FormFunctions.updatePicker, "", "Todas las campañas"
    );

    $('#agentInput').selectpicker(
        {
            "liveSearch": true
        }
    );

    FormFunctions.setAjaxLoadPicker(
        '#agentInput', picker_search_agent_url, 
        FormFunctions.updatePicker, "Todos los agentes"
    );
    
    FormFunctions.ajaxLoadPicker(
        '#agentInput', picker_search_agent_url, 
        FormFunctions.updatePicker, "", "Todos los agentes"
    );

    urls = {
        'get_data_dashboard_url': {'url' : get_data_dashboard_url, 'method':'POST'},
        'get_data_dashboard_out_url': {'url' : get_data_dashboard_out_url, 'method':'POST'},
    }
    standard = new StandardCrud(urls);

    var now = new Date();

    var day = ("0" + now.getDate()).slice(-2);
    var month = ("0" + (now.getMonth() + 1)).slice(-2);

    var today = now.getFullYear()+"-"+(month)+"-"+(day) ;

    $('#startDateInput').val(today);
    $('#endDateInput').val(today);

    getData();
});