var call_consolidacion_id; 
var data_email;
var inTransaction = false;
var reset = false;
var stateChanged = false;

function getValues(){
    data = {
        'cedula': $('#cedulaInput').val(),
        'placa': $('#placaInput').val(),
        'sede': $('#sedeInput').val(),
        'fecha': $('#fechaInput').val(),
        'hora': $('#horaInput').val(),
        'motivo': $('#motivoInput').val(),
        'call_consolidacion_id': $('#call_consolidacion_idInput').val(),
    }
    data_email = data;
    return data;
}

function getAgentState(agent, previous_state, previous_call){ 
    console.log(inTransaction);
    console.log(reset);

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
                if(result.update && !inTransaction){
                    $('#lblStatus').html(result.status);
                    $('#lblMessage').html(result.message);
                    if(result.call){
                        inTransaction = true;
                        $('#contentCita').removeClass('d-none');
                        $('#contentEmail').addClass('d-none');
                        $('#fechaInput').val("");
                        $('#successModal').modal('show');
                        $('#successModal').modal({backdrop:'static', keyboard:false});
                    }
                    previous_state = result.previous;
                    if(result.call){
                        previous_call = result.llamada_id;
                        data = {'data':result}
                        Citas.setCallConsolidacionId(result.call_consolidacion_id);
                        StandardCrud.standardSetValues(data);
                    }
                }
                if(result.update){
                    stateChanged = true;
                }
            },
            complete: function(){
                setTimeout(function(){ 
                    if(reset){
                        getAgentState(agent, -1, previous_call);
                        reset = false;
                    }
                    else{
                        getAgentState(agent, previous_state, previous_call);
                    }
                }, 1000);
            },
        });
    }
    else{
        $('#lblStatus').html("No es agente");
        $('#lblMessage').html("No hay un agente ligado a este usuario");
    }
}


$( document ).ready(function() {
    $('#horaInput').prop('disabled', 'disabled');
    $('#sedeInput').selectpicker({"liveSearch": true});
    $('#motivoInput').selectpicker({"liveSearch": true});
    $('#generarCitaButton').click(Citas.createCita);
    $('#gotoCitasTallerButton').click(Citas.goToCitasTaller);
    $('#emailButton').click(Citas.sendConfirmationEmail);
    $('#sedeInput').change(Citas.getHorariosDisponibles);
    $('#fechaInput').change(Citas.getHorariosDisponibles);
    $('#fechaInput').change(Citas.getHorariosDisponibles);
    $('#noEmailButton').click(Citas.cancel);
    $('#cancelButton').click(Citas.cancel);

    urls = {
        'get_motivo_url': {'url' : get_motivo_url, 'method':'POST'},
        'get_sede_url': {'url' : get_sede_url, 'method':'POST'},
        'create_cita_url': {'url' : create_cita_url, 'method':'POST'},
        'check_horarios': {'url' : check_horarios_url, 'method':'POST'},
        'send_confirmation_mail_url': {'url' : send_confirmation_mail_url, 'method':'POST'},
    }

    Citas.standard = new StandardCrud(urls);;

    FormFunctions.setAjaxLoadPicker('#sedeInput', picker_search_sede_url, Citas.updatePickerSede, "Escoja una sede");
    FormFunctions.setAjaxLoadPicker('#motivoInput', picker_search_motivo_url, FormFunctions.updatePicker, "Escoja un motivo");
    FormFunctions.ajaxLoadPicker('#sedeInput', picker_search_sede_url, Citas.updatePickerSede, "", "Escoja una sede");
    FormFunctions.ajaxLoadPicker('#motivoInput', picker_search_motivo_url, FormFunctions.updatePicker, "", "Escoja un motivo");

    setTimeout(function(){ 
        getAgentState(id_agent, -1, "");
    }, 1000);
});
