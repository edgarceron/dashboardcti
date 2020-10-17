var urls;
var errorFields = [];
var standard;

function getValues(){
    data = {
        "name": $('#nameInput').val(),
        "type_campaign" : $('#type_campaignInput').val(),
        "form" : $('#formInput').val(),
        "isabel_campaign" : $('#isabel_campaignInput').val(),
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
            var type = result.data.type_campaign;
            console.log(type);
            changeTypeCampaign(type);
            standard.standardSetValues(result);
        },
        'error': function(result){
            standard.standardGetError(result);
        }
    }
    standard.makePetition(null, 'get_url', ajaxFunctions);
}

function setLoaderIsabelCampaign(url_picker, url_get){
    standard.urls['get_isabel_campaign_url'] = {'url' : url_get, 'method':'POST'};
    $('#isabel_campaignInput').siblings().find("input[type='text']").unbind('keydown');
    FormFunctions.setAjaxLoadPicker(
        '#isabel_campaignInput', url_picker, FormFunctions.updatePicker, "Escoja una campaña"
    );
    FormFunctions.ajaxLoadPicker(
        '#isabel_campaignInput', url_picker, FormFunctions.updatePicker, "", "Escoja una campaña"
    );
    $('#isabel_campaignInput')
        .removeAttr('readonly') 
        .val("")
        .selectpicker('refresh')
    ;
}

function changeTypeCampaign(type){
    if( type == 1){
        setLoaderIsabelCampaign(picker_search_campaign_url, get_campaign_url);
    }
    else if( type == 2){
        setLoaderIsabelCampaign(picker_search_campaign_entry_url, get_campaign_entry_url);
    }
    else if( type == 0){
        $('#isabel_campaign')
            .find('option')
            .remove()
            .end()
            .append('<option value="">Escoja una campaña</option>')
            .val("")
            .selectpicker('refresh')
            .attr('readonly', 'readonly')
        ;
    }
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
        'get_form_url': {'url' : get_form_url, 'method':'PUT'},
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

    $('#type_campaignInput').change(function(){
        changeTypeCampaign($('#type_campaignInput').val());
    });

    $('#formInput').selectpicker(
        {
            "liveSearch": true
        }
    );

    $('#isabel_campaignInput').selectpicker(
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