var urls;
var errorFields = [];
var standard;

function getValues(){
    data = {
        'name': $('#nameInput').val(),
        "type_campaign" : $('#type_campaignInput').val(),
        "form" : $('#formInput').val(),
    }
    return data;
}

function saveCampaign(){
    var ajaxFunctions = {
        'success': function(result){
            FormFunctions.resetFormErrors(errorFields);
            errorFields = [];
            $('#successModal').modal('toggle');
            $('#successModal').modal({backdrop:'static', keyboard:false}); 
            setTimeout(function(){ 
                $(location).attr('href', listing_url);
            }, 2000);
        },
        'error': standard.standardError
    }
    standard.makePetition(getValues(), 'add_url', ajaxFunctions);
}

function updateCampaign(){
    var ajaxFunctions = {
        'success': function(result){
            FormFunctions.resetFormErrors(this.errorFields);
            this.errorFields = [];
            $('#successModal').modal('toggle');
            $('#successModal').modal({backdrop:'static', keyboard:false}); 
            setTimeout(function(){ 
                $(location).attr('href', listing_url);
            }, 2000);
        },
        'error': standard.standardError
    }
    standard.makePetition(getValues(), 'replace_url', ajaxFunctions);
}

function getDataCampaign(){
    var ajaxFunctions = {
        'success': function(result){
            standard.standardSetValues(result);
        },
        'error': function(result){
            standard.standardGetError(result);
        }
    }
    standard.makePetition(null, 'get_url', ajaxFunctions);
}

$( document ).ready(function() {
    if(id != 0){
        get_url = get_url + id;
        replace_url = replace_url + id;
    }
    
    urls = {
        'listing_url': {'url': listing_url},
        'add_url': {'url' : add_url, 'method':'POST'},
        'get_url': {'url' : get_url, 'method':'POST'},
        'replace_url': {'url' : replace_url, 'method':'PUT'},
        'get_form_url': {'url' : get_form_url, 'method':'PUT'}
    }
    standard = new StandardCrud(urls);

    $('#saveButton').click(function(){
        if(id != 0){
            updateCampaign();
        }
        else{
            saveCampaign();
        }
    });

    $('#formInput').selectpicker(
        {
            "liveSearch": true
        }
    );

    FormFunctions.setAjaxLoadPicker(
        '#formInput', picker_search_form_url, FormFunctions.updatePicker, "Escoja un formulario"
    );

    FormFunctions.ajaxLoadPicker(
        '#formInput', picker_search_form_url, FormFunctions.updatePicker, "", "Escoja un formulario"
    );

    if(id!=0){
        getDataCampaign();
    }

});