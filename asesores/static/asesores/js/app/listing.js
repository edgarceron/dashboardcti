var standard;
var urls;

function deleteAsesor(asesor_id){
    urls['delete_url'] = {'url' : delete_url + asesor_id, 'method':'DELETE'};
    standard = new StandardCrud(urls);
    var ajaxFunctions = {
        'success': function(result){
            standard.standardDeleteSuccess("Asesor");
        },
        'error': function(result){
            SoftNotification.show(result.responseJSON.message,"danger");
        }
    }
    standard.makePetition(null, 'delete_url', ajaxFunctions);
}

function toogleAsesorState(asesor_id, square_element){
    console.log(asesor_id);
    urls['toggle_url'] = {'url' : toggle_url + asesor_id, 'method':'POST'};
    standard = new StandardCrud(urls);
    var ajaxFunctions = {
        'success': function(result){
            standard.standardToggleSuccess(result, square_element, "Asesor");
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
    
    standard.standardDatatable(columns, deleteAsesor, toogleAsesorState);
} );