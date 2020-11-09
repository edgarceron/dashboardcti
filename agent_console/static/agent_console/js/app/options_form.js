var urls;
var errorFields = [];
var standard;

function getValues(){
    var values={
        'CAMPAIGN_CONSOLIDACION':$('#CAMPAIGN_CONSOLIDACIONInput').val(),
    }
    return values;
}

function updateData(){

    var ajaxFunctions = {
        'success': function(result){
            if(result.success){
                SoftNotification.show("Opciones guardadas con exito");
            }
        },
        'error': standard.standardError
    }
    standard.makePetition(getValues(), 'replace_options_agent_console_url', ajaxFunctions);
}

function loadTimes(){
    var dom_name = "";
    for(b in breaK_time_data){
        dom_name = "#break_input" + b;
        $(dom_name).val(breaK_time_data[b])
    }
}

function saveBreakAllowedTimes(){
    var data = []
    var dom_name = "";
    console.log(break_data);
    for(b of break_data){
        dom_name = "#break_input" + b;
        data.push({'id_break': b, 'minutes': $(dom_name).val()});
    }

    var ajaxFunctions = {
        'success': function(result){
            if(result.success){
                SoftNotification.show("Tiempos permitidos de descanso guardados con exito");
            }
        },
        'error': standard.standardError
    }
    data = JSON.stringify(data);
    standard.makePetition({'breaks': data}, 'save_break_times_url', ajaxFunctions);

}

function getData(user_id){
    var ajaxFunctions = {
        'success': function(result){
            standard.standardSetValues(result);
        },
        'error': function(result){
            standard.standardGetError(result);
        }
    }
    standard.makePetition(null, 'get_options_agent_console_url', ajaxFunctions);
}

function autoGenerateUsers(){
    $.ajax({
        url: auto_generate_users_url,
        method: 'POST',
        async: false,
        dataType: 'json',
        data: {},
        beforeSend: function(){},
        success: function(result){
            if(result.success){
                SoftNotification.show(result.message);
            }
            else{
                SoftNotification.show(result.message, "danger");
            }
        },
        error: function (request, status, error){},
        complete: function(){},
    });
}

function generateCallsConsolidacion(){
    $.ajax({
        url: create_calls_asterisk_url,
        method: 'POST',
        async: false,
        dataType: 'json',
        data: {},
        beforeSend: function(){},
        success: function(result){
            if(result.success){
                SoftNotification.show(result.message);
            }
            else{
                SoftNotification.show(result.message, "danger");
            }
        },
        error: function (request, status, error){},
        complete: function(){},
    });
}


$( document ).ready(function() {

    urls = {
        'get_options_agent_console_url': {'url' : get_options_agent_console_url, 'method':'POST'},
        'replace_options_agent_console_url': {'url' : replace_options_agent_console_url, 'method':'PUT'},
        'get_CAMPAIGN_CONSOLIDACION_url': {'url' : get_campaign_url, 'method':'POST'},
        'add_break': {'url' : add_break, 'method':'PUT'},
        'save_break_times_url': {'url' : save_break_times_url, 'method':'POST'},
    }
    standard = new StandardCrud(urls);

    $('#saveButton').click(function(){
        updateData();
    });

    $('#saveButton_b').click(function(){
        saveBreakAllowedTimes();
    });

    $('#generateButton').click(function(){
        autoGenerateUsers();
    });

    $('#callsConsolidacionButton').click(function(){
        generateCallsConsolidacion();
    });

    $('#CAMPAIGN_CONSOLIDACIONInput').selectpicker(
        {
            "liveSearch": true
        }
    );

    FormFunctions.setAjaxLoadPicker(
        '#CAMPAIGN_CONSOLIDACIONInput', picker_search_campaign_url, 
        FormFunctions.updatePicker, "Seleccione una campaña"
    );
    FormFunctions.ajaxLoadPicker(
        '#CAMPAIGN_CONSOLIDACIONInput', picker_search_campaign_url, 
        FormFunctions.updatePicker, "Seleccione una campaña"
    );
    
    
    getData();
    loadTimes();
});