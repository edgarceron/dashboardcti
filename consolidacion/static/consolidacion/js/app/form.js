var urls;
var errorFields = [];
var standard;

function getValues(){
    data = {
        'cedula': $('#cedulaInput').val(),
        'placa': $('#placaInput').val(),
        'fecha': $('#fechaInput').val(),
        'motivo': $('#motivoInput').val(),
    }
    return data;
}

function validateCedula(){
    var ajaxFunctions = {
        'success': function(result){
            if(result.success){
                $('#nombreCliente').html(result.nombre);
                $('#placaCliente').html($('#placaInput').val());
                $('#cautionModal').modal('toggle');
            }
            else {
                SoftNotification.show(result.message);
            }
        },
        'error': standard.standardError
    }
    standard.makePetition(getValues(), 'validate_cedula_url', ajaxFunctions);
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
    if(id != 0){
        get_url = get_url + id;
        replace_url = replace_url + id;
    }
    
    urls = {
        'listing_url': {'url': listing_url},
        'add_url': {'url' : add_url, 'method':'POST'},
        'get_url': {'url' : get_url, 'method':'POST'},
        'replace_url': {'url' : replace_url, 'method':'PUT'},
        'get_motivo_url': {'url' : get_motivo_url, 'method':'PUT'},
        'validate_cedula_url': {'url' : validate_cedula_url, 'method':'POST'}
    }
    standard = new StandardCrud(urls);

    $('#saveButton').click(function(){
        validateCedula()
    });

    $('#confirmButton').click(function(){
        if(id != 0){
            updateForm();
        }
        else{
            saveForm();
        }
    });

    $('#motivoInput').selectpicker(
        {
            "liveSearch": true
        }
    );

    if(id!=0){
        getDataForm();
    }

    FormFunctions.setAjaxLoadPicker('#motivoInput', picker_search_motivo_url, FormFunctions.updatePicker, "Escoja un motivo");
    FormFunctions.ajaxLoadPicker('#motivoInput', picker_search_motivo_url, FormFunctions.updatePicker, "", "Escoja un motivo");
});