var data_email;

function getValues(){
    data = {
        'cedula': $('#cedulaInput').val(),
        'placa': $('#placaInput').val(),
        'sede': $('#sedeInput').val(),
        'fecha': $('#fechaInput').val(),
        'hora': $('#horaInput').val(),
        'motivo': $('#motivoInput').val(),
        'observaciones': $('#observacionesInput').val(),
        'call_consolidacion_id': $('#call_consolidacion_idInput').val(),
        'id_call_entry': AgentConsole.llamada_id,
    }
    data_email = data;
    return data;
}

$( document ).ready(function() {
    $('#horaInput').prop('disabled', 'disabled');
    $('#sedeInput').selectpicker({"liveSearch": true});
    $('#motivoInput').selectpicker({"liveSearch": true});
    $('#motivoReagendadoInput').selectpicker({"liveSearch": true});
    $('#generarCitaButton').click(Citas.createCita);
    $('#gotoCitasTallerButton').click(Citas.goToCitasTaller);
    $('#emailButton').click(Citas.sendConfirmationEmail);
    $('#sedeInput').change(Citas.getHorariosDisponibles);
    $('#fechaInput').change(Citas.getHorariosDisponibles);
    $('#fechaInput').change(Citas.getHorariosDisponibles);
    $('#noEmailButton').click(Citas.cancel);
    $('#cancelCitaButton').click(Citas.cancel);
    $('#cancelButton').click(Citas.cancel);

    urls = {
        'get_motivo_url': {'url' : get_motivo_url, 'method':'POST'},
        'get_sede_url': {'url' : get_sede_url, 'method':'POST'},
        'create_cita_url': {'url' : create_cita_url, 'method':'POST'},
        'check_horarios': {'url' : check_horarios_url, 'method':'POST'},
        'send_confirmation_mail_url': {'url' : send_confirmation_mail_url, 'method':'POST'},
        'check_placa_url': {'url' : check_placa_url, 'method':'POST'},
        'check_tercero_cedula_url': {'url' : check_tercero_cedula_url, 'method':'POST'},
    }

    Citas.standard = new StandardCrud(urls);

    $('#cedulaInput').change(function(){
        var cedula = $('#cedulaInput').val();
        Citas.validateCedula(cedula);
    });

    $('#placaInput').change(function(){
        var placa = $('#placaInput').val();
        Citas.validatePlaca(placa);
    });
    
    FormFunctions.setAjaxLoadPicker('#sedeInput', picker_search_sede_url, Citas.updatePickerSede, "Escoja una sede");
    FormFunctions.setAjaxLoadPicker('#motivoInput', picker_search_motivo_url, FormFunctions.updatePicker, "Escoja un motivo");
    FormFunctions.setAjaxLoadPicker('#motivoReagendadoInput', picker_search_motivo_url, FormFunctions.updatePicker, "Escoja un motivo");
    FormFunctions.ajaxLoadPicker('#sedeInput', picker_search_sede_url, Citas.updatePickerSede, "", "Escoja una sede");
    FormFunctions.ajaxLoadPicker('#motivoInput', picker_search_motivo_url, FormFunctions.updatePicker, "", "Escoja un motivo");
    FormFunctions.ajaxLoadPicker('#motivoReagendadoInput', picker_search_motivo_url, FormFunctions.updatePicker, "", "Escoja un motivo");
    
});