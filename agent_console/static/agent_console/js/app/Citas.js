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
                SoftNotification.show('Cita creada con exito');
                $('#successModal').modal('hide');
                setTimeout(function(){ 
                    $('#contentTeceros').addClass('d-none');
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
        Citas.standard.makePetition(getValues(), 'create_cita_url', ajaxFunctions);
    }

    static sendConfirmationEmail(){
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
        Citas.standard.makePetition(data_email, 'send_confirmation_mail_url', ajaxFunctions);
    }

    
    static cancel(){
        Citas.endTransaction();
        $('#successModal').modal('hide');
    }

    static endTransaction(){
        inTransaction = false;
        if(stateChanged){
            reset = true;
            stateChanged = false;
        } 
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
                    SoftNotification.show("No existe un tercero con esta cedula");
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
                    SoftNotification.show("No existe esta placa en el sistema");
                }
            },
            'error': function(request, status, error){
                SoftNotification.show("Sucedio un error al intentar verificar la placa", "danger");
            }
        }
        Citas.standard.makePetition(data, 'check_placa_url', ajaxFunctions);
    }
}