var standard;
var urls;

function deleteForm(form_id){
    urls['delete_url'] = {'url' : delete_url + form_id, 'method':'DELETE'};
    standard = new StandardCrud(urls);
    var ajaxFunctions = {
        'success': function(result){
            standard.standardDeleteSuccess("Formulario");
        },
        'error': function(result){
            SoftNotification.show(result.responseJSON.message,"danger");
        }
    }
    standard.makePetition(null, 'delete_url', ajaxFunctions);
}

function toogleFormState(form_id, square_element){
    console.log(form_id);
    urls['toggle_url'] = {'url' : toggle_url + form_id, 'method':'POST'};
    standard = new StandardCrud(urls);
    var ajaxFunctions = {
        'success': function(result){
            standard.standardToggleSuccess(result, square_element, "Form");
        },
        'error': function(result){
            SoftNotification.show(result.responseJSON.message,"danger");
        }
    }
    standard.makePetition(null, 'toggle_url', ajaxFunctions);
}

$(document).ready(function() {

    urls = {
        'data_list_url': {'url': data_list_url},
        'delete_url': {'url' : delete_url, 'method':'DELETE'},
        'toggle_url': {'url' : toggle_url, 'method':'POST'}
    }
    standard = new StandardCrud(urls);

    var columns = [
        { "data": "id" },
        { "data": "name" },
    ];
    
    standard.standardDatatable(columns, deleteForm, toogleFormState);
} );