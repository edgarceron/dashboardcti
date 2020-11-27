var urls = {};
var standard = {};
var table = null;

$('#agentInput').selectpicker(
    {
        "liveSearch": true
    }
);

function failPrepare(){
    var start_date = $('#fechaInicioInput').val();
    var end_date = $('#fechaFinInput').val();
    if(start_date == "") start_date = today_date();
    if(end_date == "") end_date = today_date();

    var data = {
        'start_date': start_date,
        'end_date': end_date
    }

    var ajaxFunctions = {
        'success': function(result){
            var color;
            if(result.success) color = "success";
            else color = "danger";
            SoftNotification.show(result.message, color);
        },
        'error': function(result){
            SoftNotification.show("Ocurrio un error", "danger");
        }
    }
    standard.makePetition(data, 'fail_prepare_url', ajaxFunctions);
}

function cancelCita(tall_cita_id){
    standard = new StandardCrud(urls);
    var ajaxFunctions = {
        'success': function(result){
            SoftNotification.show(result.message);
        },
        'error': function(result){
            SoftNotification.show(result.responseJSON.message,"danger");
        }
    }
    data = {'motivo': $('#motivoInput').val(), 'id_cita': tall_cita_id}
    standard.makePetition(data, 'cancel_cita_url', ajaxFunctions);
}

function today_date(){
    var today = new Date();
    var dd = today.getDate();

    var mm = today.getMonth()+1; 
    var yyyy = today.getFullYear();
    if(dd<10) 
    {
        dd='0'+dd;
    } 

    if(mm<10) 
    {
        mm='0'+mm;
    } 

    return yyyy + "-" + mm + "-" + dd;
}

function listingButtonsFunction(event){
    var target = event.target;
    var parent = target.parentElement;
    parent = $(parent);
    target = $(target);
    var model_id = parent.attr('model_id');
    if(target.hasClass('fa-trash')){
        $('#messageModal').html("¿Esta seguro de que quiere eliminar la cita con id");
        StandardCrud.standardDeleteConfirmation(model_id, deleteCita);
    }
    else if(target.hasClass('fa-calendar-times')){
        $('#messageModal').html("¿Esta seguro de que quiere cancelar la cita con id");
        StandardCrud.standardDeleteConfirmation(model_id, cancelCita);
    }
}

function createdRow(row, data, index){
    var count = row.cells.length 
    var data_rows = count - 2;
    var options_row = count -1;
    for(var i = 0;i < data_rows;i++){
        $('td', row).eq(i).addClass("row_object_id");
        $('td', row).eq(i).attr('model_id', data.id_cita);
    }
    $('td', row).eq(options_row).attr('model_id', data.id_cita);
    
    if(data.active){
        $('.fa-square', row).addClass('fa-check-square');
        $('.fa-square', row).removeClass('fa-square');
    }
}

function tallCitaDatatable(columns){

    columns.push({ "data": function(){
        var options = "";
        options += '<i class="far fa-fw fa-calendar-times text-danger cursor-pointer" data-toggle="tooltip" data-placement="bottom" title="Cancelar cita"></i>';
        return options;
    }});

    table = $('#listing').dataTable( {
        "processing": true,
        "serverSide": true,
        "ajax": {
            "type": "POST",
            "processing": true,
            "url": listing_citas_taller_url,
            "dataSrc": "data",
            "data": function ( d ) {
                d.agent = $('#agentInput').val();
                d.start_date = $('#fechaInicioInput').val();
                d.end_date = $('#fechaFinInput').val();
                d.date_type = $('#selectTypeDate').val();
            }
        },

        "createdRow": function ( row, data, index ) {
            createdRow(row, data, index)
        },

        "columns": columns, 

        "lengthMenu": [[10, 25, 50], [10, 25, 50]],

        "drawCallback": function( settings ) {
            $('.row_object_id').dblclick(function(event){
                var target = $(event.delegateTarget);
                var id = target.attr('model_id');
                window.location = update_url + id;
            });

            $('.fa-trash, .fa-calendar-times').click(function(event){
                listingButtonsFunction(event);
            });

            $('.row_object_id').css('cursor', 'pointer'); 

            $(function () {
                $('[data-toggle="popover"]').popover()
            });
        }
    });

    console.log(table.api().ajax);

    $('#listing tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
    });
}

$( document ).ready(function() {

    urls = {
        'fail_prepare_url': {'url' : fail_prepare_url, 'method':'POST'},
        'listing_citas_taller_url': {'url' : listing_citas_taller_url, 'method':'POST'},
        'cancel_cita_url': {'url' : cancel_cita_url, 'method':'POST'},   
    }
    standard = new StandardCrud(urls);

    FormFunctions.setAjaxLoadPicker(
        '#agentInput', pircker_search_agent_url, FormFunctions.updatePicker, "Todos los agentes"
    );

    FormFunctions.ajaxLoadPicker(
        '#agentInput', pircker_search_agent_url, FormFunctions.updatePicker, "", "Todos los agentes"
    );

    $('#downloadButton').click(function(){
        var start_date = $('#fechaInicioInput').val();
        var end_date = $('#fechaFinInput').val();  
        var agent = $('#agentInput').val();
        var date_type = $('#selectTypeDate').val();
        var url = download_consolidaciones_url;
        var today = new Date();
        if(start_date == "") start_date = "empty";
        if(end_date == "") end_date = "empty";
        if(agent == "") agent = "0";
        url = url.replace("abc", start_date);
        url = url.replace("def", end_date);
        url = url.replace("123", date_type);
        window.location.href = url;
    });

    $('#downloadFailsButton').click(function(){
        var start_date = $('#fechaInicioInput').val();
        var end_date = $('#fechaFinInput').val();
        var url = download_fails_url;
        var today = new Date();
        if(start_date == "") start_date = today_date();
        if(end_date == "") end_date = today_date();
        url = url.replace("abc", start_date);
        url = url.replace("def", end_date);
        window.location.href = url;
    });

    $('#filterButton').click(function(){
        table.api().ajax.reload();
    });

    $('#reCallButton').click(function(){
        failPrepare();
    });
    
    var columns = [
        { "data": "nit"},
        { "data": "placa"},
        { "data": "bodega"},
        { "data": "nombre_cliente"},
        { "data": "nombre_encargado"},
        { "data": "fecha_hora_ini"},
        { "data": "telefonos"},
        { "data": "mail"},
        { "data": "estado_cita"},
    ];

    tallCitaDatatable(columns);
});