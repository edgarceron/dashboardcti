//TODO
//Ajax webservice usuarios
var id;
var listing_url;
var errorFields = [];
var singleOperationRestriction = false;

saveSuccess = function(result){
    if(result.success){
        FormFunctions.resetFormErrors(errorFields);
        errorFields = [];
        $('#successModal').modal('toggle');
        $('#successModal').modal({backdrop:'static', keyboard:false}); 
        setTimeout(function(){ 
            $(location).attr('href', listing_url);
        }, 2000);
    }
}

function getValues(){
    data = {
        "name"    : $('#nameInput').val(),
        "lastname": $('#lastnameInput').val(),
        "username": $('#usernameInput').val(),
        "password": $('#passwordInput').val(),
        "active"  : $('#activeInput').prop('checked'),
        "profile" : $('#profileInput').val()
    }
    return data;
}

function addData(){
    var ajaxFunctions = {
        'success': function(result){
            saveSuccess(result);
        },
        'error': standard.standardError
    }
    standard.makePetition(getValues(), 'add_url', ajaxFunctions);
}
/*
function addData(){
    if(!singleOperationRestriction){
        singleOperationRestriction = true;
        $.ajax({
            url: add_url,
            method: "POST",
            async: false,
            dataType: "json",
            data: {
                "name"    : $('#nameInput').val(),
                "lastname": $('#lastnameInput').val(),
                "username": $('#usernameInput').val(),
                "password": $('#passwordInput').val(),
                "active"  : $('#activeInput').prop('checked'),
                "profile" : $('#profileInput').val()
            },
            beforeSend: function(){

            },
            success: function(result){
                saveSuccess(result);
            },
            error: function (request, status, error, result){
                var details = request.responseJSON.Error.details;
                FormFunctions.resetFormErrors(errorFields);
                errorFields = [];
                FormFunctions.setFormErrors(details);
            },
            complete: function(){
                singleOperationRestriction = false;
            }
        });
    }
}
*/

function updateData(){
    var ajaxFunctions = {
        'success': function(result){
            saveSuccess(result);
        },
        'error': standard.standardError
    }
    standard.makePetition(getValues(), 'replace_url', ajaxFunctions);
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
    standard.makePetition(null, 'get_url', ajaxFunctions);
}

function saveFunction(){
    if(id == 0){
        saveForm();
    }
    else{
        updateData(id);
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
        'get_profile_url': {'url' : get_profile_url, 'method':'POST'},
    }
    standard = new StandardCrud(urls);

    $('#saveButton').click(function(){
        saveFunction();
    });

    $('#profileInput').selectpicker(
        {
            "liveSearch": true
        }
    );

    FormFunctions.setAjaxLoadPicker(
        '#profileInput', picker_search_profile_url, FormFunctions.updatePicker, "Ningún perfil"
    );
    FormFunctions.ajaxLoadPicker(
        '#profileInput', picker_search_profile_url, FormFunctions.updatePicker, "", "Ningún perfil"
    );

    if(id != 0){
        getData(id);
        $('#passwordInput').attr("placeholder", "Ingrese aquí una nueva contraseña temporal");
    }

});