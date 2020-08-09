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
    standard.makePetition(getValues(), 'replace_options_dashboard_url', ajaxFunctions);
}

function getData(){
    var ajaxFunctions = {
        'success': function(result){
            standard.standardSetValues(result);
        },
        'error': function(result){
            standard.standardGetError(result);
        }
    }
    standard.makePetition(null, 'get_options_dashboard_url', ajaxFunctions);
}

$( document ).ready(function() {

    urls = {
        'get_options_dashboard_url': {'url' : get_options_dashboard_url, 'method':'POST'},
        'replace_options_dashboard_url': {'url' : replace_options_dashboard_url, 'method':'PUT'}
    }
    standard = new StandardCrud(urls);

    $('#saveButton').click(function(){
        updateData();
    });

    getData();
});