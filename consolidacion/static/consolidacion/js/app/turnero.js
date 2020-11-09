var urls;
var standard;

$('#sedeInput').selectpicker(
    {
        "liveSearch": true
    }
);

function getTurnoHtml(pos, nombre, hora){
    var html = 
    `
    <div class="row">
        <div class="col-3 bg-primary text-white text-center">
            <h1>${pos}</h1>
        </div>
        <div class="col-6 border">
            <h3>${nombre}</h3>
        </div>
        <div class="col-3 border">
            <h3>${hora}</h3>
        </div>
    </div>
    `;
    return html;
}

function putTurnos(turnos){
    var pos = 1;
    var html;
    $('#turnosContainer').empty();
    for(x of turnos){
        html = getTurnos(pos, x.nombre_cliente, x.fecha_hora_ini);
        $('#turnosContainer').append(html);
    }
}

function getTurnos(){
    var data = {'sede': $('#sedeInput').val()}
    var ajaxFunctions = {
        'success': function(result){
            if(result.success) putTurnos(result.turnos);
        },
        'error': function(result){

        }
    }
    standard.makePetition(data, 'get_closest_turns_url', ajaxFunctions);
}

$( document ).ready(function() {

    urls = {
        'get_closest_turns_url': {'url' : get_closest_turns_url, 'method':'POST'},
    }

    standard = new StandardCrud(urls);

    FormFunctions.setAjaxLoadPicker(
        '#sedeInput', picker_search_sede_url, FormFunctions.updatePicker, "Escoja una sede"
    );

    FormFunctions.ajaxLoadPicker(
        '#sedeInput', picker_search_sede_url, FormFunctions.updatePicker, "", "Escoja una sede"
    );

    $('#sedeInput').change(function(){
        getTurnos();
    });
    
    getTurnos();

    setInterval(function(){
        getTurnos();
    }, 60000);

})