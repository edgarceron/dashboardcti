function getValues(){
    var data = {
        'id_agent':'',//$('#id_agentInput').val(),
        'id_campaign':'',//$('#id_campaignInput').val(),
        'start_date':$('#start_dateInput').val(),
        'end_date':$('#end_dateInput').val(),
    }
    return data;
}

function getData(){
    standard.async = true;
    var ajaxFunctions = {
        'success': function(result){
            drawHoursChart(result.call_entry_per_hour);
            drawTmoChart(result.tmo, result.seconds);
            drawEffectivenessChart(result.effectiveness);
            drawServiceLevelChart(result.service_level, result.seconds);
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

    urls = {
        'get_data_dashboard_url': {'url' : get_data_dashboard_url, 'method':'POST'},
    }
    standard = new StandardCrud(urls);

    var now = new Date();

    var day = ("0" + now.getDate()).slice(-2);
    var month = ("0" + (now.getMonth() + 1)).slice(-2);

    var today = now.getFullYear()+"-"+(month)+"-"+(day) ;

    $('#start_dateInput').val(today);
    $('#end_dateInput').val(today);
    getData();
});