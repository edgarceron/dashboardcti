
function getValues(){
    data = {
        'cedula': $('#cedulaInput').val(),
        'placa': $('#placaInput').val(),
        'sede': $('#sedeInput').val(),
        'fecha': $('#fechaInput').val(),
        'hora': $('#horaInput').val(),
        'motivo': $('#motivoInput').val(),
    }
    return data;
}

function getHorariosDisponibles(){
    data = {
        'sede': $('#sedeInput').val(),
        'fecha': $('#fechaInput').val()
    }
    $('#horaInput').prop('disabled', 'disabled');
    standard.async = true;
    var ajaxFunctions = {
        'success': function(result){
            var horarios = result.horarios
            $('#horaInput').empty();
            horarios.forEach(element => {
                $('#horaInput').append($('<option>').val(element).text(element));
            });
            $('#horaInput').prop('disabled', false);
        },
        'error': function(request, status, error){
            var result = request.responseJSON
            if($('#fechaInput').val() != ""){
                SoftNotification.show(result.message, 'danger');
            }
            $('#horaInput').empty();
        }
    }
    standard.makePetition(getValues(), 'check_horarios', ajaxFunctions);
    standard.async = false;
}

function getAgentState(agent, previous_state, previous_call){ 
    if(agent != null){
        $.ajax({
            url: agent_state_url,
            method: 'POST',
            async: true,
            dataType: 'json',
            data: {
                'id_agent': agent,
                'previous_state':previous_state,
                'previous_call':previous_call
            },
            success: function(result){
                if(result.update){
                    $('#lblStatus').html(result.status);
                    $('#lblMessage').html(result.message);
                    if(result.call){
                        $('#successModal').modal('show');
                        $('#successModal').modal({backdrop:'static', keyboard:false}); 
                    }                    
                    previous_state = result.previous;
                    if(result.call){
                        previous_call = result.llamada_id;
                        data = {'data':result}
                        standard.standardSetValues(data);
                    }
                }
            },
            complete: function(){
                setTimeout(function(){ 
                    getAgentState(agent, previous_state, previous_call);
                }, 1000);
            },
        });
    }
    else{
        $('#lblStatus').html("No es agente");
        $('#lblMessage').html("No hay un agente ligado a este usuario");
    }
}

function createCita(){
    var ajaxFunctions = {
        'success': function(result){
            SoftNotification.show('Cita creada con exito');
        },
        'error': function(request, status, error, result){
            console.log(status);
            var data = result.data;
            SoftNotification.show('Hubo un error al crear la cita');
            console.log(data['crm_cita_data']);
            console.log(data['tall_cita_data']);
        }
    }
    standard.makePetition(getValues(), 'create_cita_url', ajaxFunctions);
}

function updatePickerSede(pickerName, resultados, null_value=""){
    var input = $(pickerName);
    input.html('');
    var opVal;
    var opText;

    if(null_value != ""){
        FormFunctions.addOption(input, "", null_value);
    }

    for(let data of resultados){
        opVal = data.id;
        opText = data.name + " " + data.address;
        FormFunctions.addOption(input, opVal, opText);
    }
    input.selectpicker("refresh");
}

$( document ).ready(function() {

    $('#horaInput').prop('disabled', 'disabled');
    $('#sedeInput').selectpicker(
        {
            "liveSearch": true
        }
    );

    $('#motivoInput').selectpicker(
        {
            "liveSearch": true
        }
    );

    $('#generarCitaButton').click(
        function(){
            createCita();
        }
    );

    $('#sedeInput').change(
        function(){
            console.log("YEAH");
            getHorariosDisponibles();
        }
    );

    $('#fechaInput').change(
        function(){
            console.log("YEAH");
            getHorariosDisponibles();
        }
    );

    urls = {
        'get_motivo_url': {'url' : get_motivo_url, 'method':'POST'},
        'get_sede_url': {'url' : get_sede_url, 'method':'POST'},
        'create_cita_url': {'url' : create_cita_url, 'method':'POST'},
        'check_horarios': {'url' : check_horarios_url, 'method':'POST'},
    }
    standard = new StandardCrud(urls);

    FormFunctions.setAjaxLoadPicker('#sedeInput', picker_search_sede_url, updatePickerSede, "Escoja una sede");
    FormFunctions.setAjaxLoadPicker('#motivoInput', picker_search_motivo_url, FormFunctions.updatePicker, "Escoja un motivo");
    FormFunctions.ajaxLoadPicker('#sedeInput', picker_search_sede_url, updatePickerSede, "", "Escoja una sede");
    FormFunctions.ajaxLoadPicker('#motivoInput', picker_search_motivo_url, FormFunctions.updatePicker, "", "Escoja un motivo");

    setTimeout(function(){ 
        getAgentState(id_agent, -1, "");
    }, 1000);
});
