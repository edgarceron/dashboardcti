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
        'call_consolidacion_id': call_consolidacion_id,
    }
    data_email = data;
    return data;
}

function setCallConsolidacionId(id){
    call_consolidacion_id = id;
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
                        setCallConsolidacionId(result.call_consolidacion_id);
                        standard.standardSetValues(data);
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

function createCita(){
    var ajaxFunctions = {
        'success': function(result){
            SoftNotification.show('Cita creada con exito');
            $('#successModal').modal('hide');
            setTimeout(function(){ 
                $('#contentCita').addClass('d-none');
                $('#contentEmail').removeClass('d-none');
                $('#successModal').modal('toggle');
            }, 1001);   
        },
        'error': function(request, status, error){
            console.log(status);
            if(request.responseJSON !== undefined){
                var data = request.responseJSON;
                SoftNotification.show('Hubo un error al crear la cita');
                console.log(data['crm_cita_data']);
                console.log(data['tall_cita_data']);
            }
            else{
                SoftNotification.show('Hubo un error en el servidor');
            }
        }
    }
    standard.makePetition(getValues(), 'create_cita_url', ajaxFunctions);
}

function sendConfirmationEmail(){
    var ajaxFunctions = {
        'success': function(result){
            if(result.success){
                SoftNotification.show('Correo enviado con exito');
            }
            else{
                SoftNotification.show("El cliente no tiene una dirección de correo registrada o no existe");
            }
        },
        'error': function(request, status, error, result){
            console.log(status);
            SoftNotification.show('Hubo un error al enviar el correo','danger');
        },
        'complete': function(){
            endTransaction();
        }
    }
    standard.makePetition(data_email, 'send_confirmation_mail_url', ajaxFunctions);
}

function cancel(){
    endTransaction();
    $('#successModal').modal('hide');
}

function endTransaction(){
    inTransaction = false;
    if(stateChanged){
        reset = true;
        stateChanged = false;
    } 
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

function goToCitasTaller(){
    var url = "https://www.renaultcali.com/citas-taller/";
    var win = window.open(url, '_blank');
    if (win) {
        win.focus();
    } else {
        alert('Por favor permita las ventanas emergentes para esta pagina');
    }
}

$( document ).ready(function() {

    $('#horaInput').prop('disabled', 'disabled');
    $('#sedeInput').selectpicker({"liveSearch": true});
    $('#motivoInput').selectpicker({"liveSearch": true});
    $('#generarCitaButton').click(createCita);
    $('#gotoCitasTallerButton').click(goToCitasTaller);
    $('#emailButton').click(sendConfirmationEmail);
    $('#sedeInput').change(getHorariosDisponibles);
    $('#fechaInput').change(getHorariosDisponibles);
    $('#fechaInput').change(getHorariosDisponibles);
    $('#noEmailButton').click(cancel);
    $('#cancelButton').click(cancel);

    urls = {
        'get_motivo_url': {'url' : get_motivo_url, 'method':'POST'},
        'get_sede_url': {'url' : get_sede_url, 'method':'POST'},
        'create_cita_url': {'url' : create_cita_url, 'method':'POST'},
        'check_horarios': {'url' : check_horarios_url, 'method':'POST'},
        'send_confirmation_mail_url': {'url' : send_confirmation_mail_url, 'method':'POST'},
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
