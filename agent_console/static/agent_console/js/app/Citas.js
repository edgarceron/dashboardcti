class Citas {
    static standard = null;

    static getHorariosDisponibles(){
        var data = {
            'sede': $('#sedeInput').val(),
            'fecha': $('#fechaInput').val()
        }
        $('#horaInput').prop('disabled', 'disabled');
        Citas.standard.async = true;
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
        Citas.standard.makePetition(getValues(), 'check_horarios', ajaxFunctions);
        Citas.standard.async = false;
    }

    static createCita(){
        var ajaxFunctions = {
            'success': function(result){
                if (result.message) SoftNotification.show(result.message);
                else SoftNotification.show('Cita creada con exito');
                $('#successModal').modal('hide');
                setTimeout(function(){ 
                    $('#contentTeceros').addClass('d-none');
                    $('#contentEmail').removeClass('d-none');
                    $('#successModal').modal('toggle');
                }, 1001);   
                $('#cedulaInput').val('');
                $('#nombreInput').val('');
                $('#placaInput').val('');
                $('#sedeInput').val("");
                $('#fechaInput').val("");
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
        Citas.standard.makePetition(getValues(), 'create_cita_url', ajaxFunctions);
    }

    static sendConfirmationEmail(){
        var ajaxFunctions = {
            'success': function(result){
                if(result.success){
                    SoftNotification.show('Correo enviado con exito a la direccion: ' + result.mail);
                }
                else{
                    SoftNotification.show(
                        "El cliente no tiene una dirección" +
                        " de correo registrada o no existe: " + result.mail);
                }
            },
            'error': function(request, status, error, result){
                console.log(status);
                SoftNotification.show('Hubo un error al enviar el correo','danger');
            },
            'complete': function(){
                Citas.endTransaction();
            }
        }
        Citas.standard.makePetition(data_email, 'send_confirmation_mail_url', ajaxFunctions);
    }

    static validateCedulaPlaca(){
        var ajaxFunctions = {
            'success': function(result){
                if(result.success){
                    singleOperationRestriction = false;
                    Citas.reagendar();
                }
                else {
                    SoftNotification.show(result.message);
                }
            },
            'error': function() {SoftNotification.show("Error al intentar validar los datos", "danger");}
        }
        var data = {
            'cedula': $('#cedulaInput').val(),
            'placa': $('#placaInput').val(),
            'fecha': $('#dateReagendarInput').val(),
            'motivo': $('#motivoReagendadoInput').val(),
            'sede': $('#sedeInput').val(),
        }
        Citas.standard.makePetition(data, 'validate_cedula_url', ajaxFunctions);
    }

    static reagendar(){
        var data = {
            'cedula': $('#cedulaInput').val(),
            'placa': $('#placaInput').val(),
            'fecha': $('#dateReagendarInput').val(),
            'motivo': $('#motivoReagendadoInput').val(),
            'sede': $('#sedeInput').val(),
        }

        var ajaxFunctions = {
            'success': function(result){
                if(result.success){
                    SoftNotification.show("Consolidación reagendada con exito");

                }
                else{
                    SoftNotification.show(result.message, "danger");
                }
            },
            'error': function() {SoftNotification.show("Ocurrio un error", "danger");}
        }
        Citas.standard.makePetition(data, 'add_consolidacion_url', ajaxFunctions);
    }

    static cancel(){
        $('#cedulaInput').val('');
        $('#nombreInput').val('');
        $('#placaInput').val('');
        $('#sedeInput').val("");
        $('#fechaInput').val("");
        $('#collapseCitas').collapse('hide');
        Citas.endTransaction();
        $('#successModal').modal('hide');
    }

    static endTransaction(){
        AgentConsole.inTransaction = false;
    }

    static updatePickerSede(pickerName, resultados, null_value=""){
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

    static goToCitasTaller(){
        var url = "https://www.renaultcali.com/citas-taller/";
        var win = window.open(url, '_blank');
        if (win) {
            win.focus();
        } else {
            alert('Por favor permita las ventanas emergentes para esta pagina');
        }
    }

    static setCallConsolidacionId(id){
        $("#call_consolidacion_idInput").val(id);
    }

    static validateCedula(cedula){
        var data = {
            'nit': cedula
        }
        var ajaxFunctions = {
            'success': function(result){
                if(!result.success){
                    SoftNotification.show("No existe un tercero con esta cedula", "danger");
                }
                else{
                    SoftNotification.show("El tercero esta creado en el sistema");
                    $('#nombreInput').val(result.nombres);
                }
            },
            'error': function(request, status, error){
                SoftNotification.show("Sucedio un error", "danger");
            }
        }
        Citas.standard.makePetition(data, 'check_tercero_cedula_url', ajaxFunctions);
    }

    static validatePlaca(placa){
        var data = {
            'placa': placa
        }
        var ajaxFunctions = {
            'success': function(result){
                if(!result.success){
                    SoftNotification.show("No existe esta placa en el sistema", "danger");
                }
                else{
                    SoftNotification.show("La placa esta registrada en el sistema")
                }
            },
            'error': function(request, status, error){
                SoftNotification.show("Sucedio un error al intentar verificar la placa", "danger");
            }
        }
        Citas.standard.makePetition(data, 'check_placa_url', ajaxFunctions);
    }

    static getAsesoresSede(){
        var sede = $('#sedeInput').val();
        FormFunctions.ajaxLoadPicker(
            '#asesorInput', picker_search_asesor_by_sede_url, 
            FormFunctions.updatePicker, sede);
    }

    static getCitasHorario(){
        var sede = $('#sedeInput').val();
        var fecha = $('#fechaInput').val();
        var hora = $('#horaInput').val();
        data = {
            'sede': sede,
            'fecha': fecha,
            'hora': hora,
        }
        var ajaxFunctions = {
            'success': function(result){
                $('#divCitasHorario').html('');
                var html;
                for(let cita of result.citas){
                    html = `
                    <div class="row">
                        <div class="col-md-3">${cita.nit}</div>
                        <div class="col-md-3">${cita.nombre_cliente}</div>
                        <div class="col-md-3">${cita.asesor}</div>
                    </div>
                    `;
                    $('#divCitasHorario').append(html);
                }
            },
            'error': function(request, status, error){
                SoftNotification.show("Sucedio un error al intentar verificar citas en el horario", "danger");
            }
        }
        Citas.standard.makePetition(data, 'check_citas_horario_url', ajaxFunctions);
    }
}