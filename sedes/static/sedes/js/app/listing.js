var standard;
var urls;

function deleteSede(sede_id){
    urls['delete_url'] = {'url' : delete_url + sede_id, 'method':'DELETE'};
    standard = new StandardCrud(urls);
    var ajaxFunctions = {
        'success': function(result){
            standard.standardDeleteSuccess("Sede");
        },
        'error': function(result){
            SoftNotification.show(result.responseJSON.message,"danger");
        }
    }
    standard.makePetition(null, 'delete_url', ajaxFunctions);
}

function toogleSedeState(sede_id, square_element){
    console.log(sede_id);
    urls['toggle_url'] = {'url' : toggle_url + sede_id, 'method':'POST'};
    standard = new StandardCrud(urls);
    var ajaxFunctions = {
        'success': function(result){
            standard.standardToggleSuccess(result, square_element, "Sede");
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
        { "data": "address"},
    ];
    
    standard.standardDatatable(columns, deleteSede, toogleSedeState);
} );