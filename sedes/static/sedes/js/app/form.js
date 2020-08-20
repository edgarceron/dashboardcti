var urls;
var errorFields = [];
var standard;

function getValues(){
    data = {
        'name': $('#nameInput').val(),
        'address': $('#addressInput').val(),
        'active': $('#activeInput').prop("checked"),
        'bodega_dms': $('#bodega_dmsInput').val()
    }
    return data;
}

function saveForm(){
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

function updateForm(){
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

function getDataForm(){
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

    $('#bodega_dmsInput').selectpicker(
        {
            "liveSearch": true
        }
    );

    if(id != 0){
        get_url = get_url + id;
        replace_url = replace_url + id;
    }
    urls = {
        'listing_url': {'url': listing_url},
        'add_url': {'url' : add_url, 'method':'POST'},
        'get_url': {'url' : get_url, 'method':'POST'},
        'get_bodega_dms_url': {'url' : get_bodega_url, 'method':'POST'},
        'replace_url': {'url' : replace_url, 'method':'PUT'},
        'replace_url': {'url' : replace_url, 'method':'PUT'},
    }
    standard = new StandardCrud(urls);

    $('#saveButton').click(function(){
        if(id != 0){
            updateForm();
        }
        else{
            saveForm();
        }
    });

    FormFunctions.setAjaxLoadPicker(
        '#bodega_dmsInput', picker_search_bodega_url, FormFunctions.updatePicker, 'Escoja una bodega'
    );
    
    FormFunctions.ajaxLoadPicker(
        '#bodega_dmsInput', picker_search_bodega_url, FormFunctions.updatePicker, "", "Escoja una bodega"
    );

    if(id!=0){
        getDataForm();
    }
});