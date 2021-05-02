var standard;
var calls_stop = false;

function getValues(){
    data = {
        "id_campaign": $('#campaignInput').val(),
        "simmultaneous" : $('#simmultaneousInput').val(),
    }
    return data;
}

function processMoreCalls(){
    var ajaxFunctions = {
        'success': function(result){
            var fails = result.data.fails;
            var pending_headers = result.data.pending_headers;
        },
        'complete': function(){
            waitForProcess();
        },
        'error': function(result){
            console.log(result);
            if(result.message) SoftNotification.show(result.message, "danger");
            else SoftNotification.show(result.message, "danger");
        }
    }
    standard.makePetition(getValues(), 'process_more_calls_url', ajaxFunctions);
}

function waitForProcess(){
    setTimeout(function(){ if(!calls_stop) processMoreCalls() }, 5000);
}

$( document ).ready(function() {
    
    urls = {
        'process_more_calls_url': {'url' : process_more_calls_url, 'method':'POST'},
    }
    standard = new StandardCrud(urls);

    $('#startButton').click(function(){
        calls_stop = false;
        processMoreCalls();
        $("#startButton").attr('disabled', true);
        $('#campaignInput').attr('disabled', true);
        $('#simmultaneousInput').attr('disabled', true);
    });

    $('#stopButton').click(function(){
        calls_stop = true;
        $("#startButton").attr('disabled', false);
        $('#campaignInput').attr('disabled', false);
        $('#simmultaneousInput').attr('disabled', false);
    });

    FormFunctions.setAjaxLoadPicker(
        '#campaignInput', picker_search_campaign_manticore_url, FormFunctions.updatePicker, "Escoja una campaña"
    );

    FormFunctions.ajaxLoadPicker(
        '#campaignInput', picker_search_campaign_manticore_url, FormFunctions.updatePicker, "", "Escoja una campaña"
    );

});