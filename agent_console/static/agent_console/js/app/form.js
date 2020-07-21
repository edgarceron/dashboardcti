/**
 * Scripts here may replace things from the users form.js
 */
var urls_additional;
var user_id; 
var urls_additional;
var standard_additional;

function getUserAgentValues(){
    var data = {
        'user': id,
        'agent': $('#agentInput').val()
    }
    return data;
}

function getUserSedeValues(){
    var data = {
        'user': id,
        'sede': $('#sedeInput').val()
    }
    return data;
}

saveSuccess = function(result){
    singleOperationRestriction = false;
    if(result.success){
        FormFunctions.resetFormErrors(errorFields);
        errorFields = [];
        id = result.id;
        setUserAgent();
        setUserSede();
    }
}

function setUserAgent(){
    var ajaxFunctions = {
        'success': function(result){
            if(result.success){
                console.log("Agente asociado con exito");
            }
            else{
                SoftNotification.show(result.message, 'danger');
            }
        },
        'error': standard_additional.standardError
    }
    standard_additional.makePetition(getUserAgentValues(), 'set_user_agent_url', ajaxFunctions);
}

function setUserSede(){
    var ajaxFunctions = {
        'success': function(result){
            if(result.success){
                $('#successModal').modal('toggle');
                $('#successModal').modal({backdrop:'static', keyboard:false}); 
                setTimeout(function(){ 
                    $(location).attr('href', listing_url);
                }, 2000);
            }
            else{
                SoftNotification.show(result.message, 'danger');
            }
        },
        'error': standard_additional.standardError
    }
    standard_additional.makePetition(getUserSedeValues(), 'set_user_sede_url', ajaxFunctions);
}

function getAgentData(id_user){ 
    urls_additional['get_agent_url'].url = get_agent_url + id_user;
    var ajaxFunctions = {
        'success': function(result){
            if(result.success){
                profile = [result.data];
                if(profile != null){
                    pickerName = '#agentInput';
                    FormFunctions.updatePicker(pickerName, profile);
                }
            }
        },
        'error': standard_additional.standardError
    }
    standard_additional.makePetition(getUserSedeValues(), 'get_agent_url', ajaxFunctions);
}

function getSedeData(id_user){ 
    urls_additional['get_user_sede_url'].url = get_user_sede_url + id_user;
    var ajaxFunctions = {
        'success': function(result){
            if(result.success){
                profile = [result.data];
                if(profile != null){
                    pickerName = '#sedeInput';
                    FormFunctions.updatePicker(pickerName, profile);
                }
            }
        },
        'error': standard_additional.standardError
    }
    standard_additional.makePetition(getUserSedeValues(), 'get_user_sede_url', ajaxFunctions);
}

$( document ).ready(function() {

    $('#agentInput').selectpicker(
        {
            "liveSearch": true
        }
    );

    $('#sedeInput').selectpicker(
        {
            "liveSearch": true
        }
    );

    urls_additional = {
        'set_user_agent_url': {'url': set_user_agent_url, 'method':'POST'},
        'set_user_sede_url': {'url': set_user_sede_url, 'method':'POST'},
        'pircker_search_agent_url': {'url': pircker_search_agent_url, 'method':'POST'},
        'pircker_search_sede_url': {'url': pircker_search_sede_url, 'method':'POST'},
        'get_agent_url': {'url': get_agent_url, 'method':'POST'},
        'get_user_sede_url': {'url': get_user_sede_url, 'method':'POST'},
    }

    standard_additional = new StandardCrud(urls_additional); 

    if(id != 0){
        getAgentData(id);
        getSedeData(id);
    }

    FormFunctions.setAjaxLoadPicker('#agentInput', pircker_search_agent_url, FormFunctions.updatePicker);
    FormFunctions.setAjaxLoadPicker('#sedeInput', pircker_search_sede_url, FormFunctions.updatePicker);
});