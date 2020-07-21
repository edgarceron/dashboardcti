var standard;
var urls;

function deleteMotivo(motivo_id){
    urls['delete_url'] = {'url' : delete_url + motivo_id, 'method':'DELETE'};
    standard = new StandardCrud(urls);
    var ajaxFunctions = {
        'success': function(result){
            standard.standardDeleteSuccess("Motivo");
        },
        'error': function(result){
            SoftNotification.show(result.responseJSON.message,"danger");
        }
    }
    standard.makePetition(null, 'delete_url', ajaxFunctions);
}

function toogleMotivoState(motivo_id, square_element){
    console.log(motivo_id);
    urls['toggle_url'] = {'url' : toggle_url + motivo_id, 'method':'POST'};
    standard = new StandardCrud(urls);
    var ajaxFunctions = {
        'success': function(result){
            standard.standardToggleSuccess(result, square_element, "Motivo");
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
        { "data": "name" }
    ];
    
    standard.standardDatatable(columns, deleteMotivo, toogleMotivoState);
} );