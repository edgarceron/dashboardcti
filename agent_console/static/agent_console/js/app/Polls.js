class Polls {
    static standard = null;
    static questionsList = [];
    static terceroValid = false;
    static isTercero = false;
    static campaign;
    static call_id;
    static data_llamada = null;
    static tercero = null;
    static header = null;

    static validateCedula(){
        var data = {'nit': $('#cedulaPollInput').val()}
        var ajaxFunctions = {
            'success': function(result){
                if(result.success){
                    $('#nombrePollInput').val(result.nombres);
                    Polls.terceroValid = true;
                }
                else {
                    Polls.terceroValid = false;
                    SoftNotification.show("No existe un cliente en DMS con esta cedula");
                }
            },
            'error': Polls.standard.standardError
        }
        Polls.standard.makePetition(data, 'check_tercero_cedula_url', ajaxFunctions);
    }

    static getQuestionObjects(form_id){
        var resultQuestions = [];
        var urls = {
            'get_questions_campaign_url': {'url' : get_questions_campaign_url + form_id, 'method':'POST'},
        }
        var standard = new StandardCrud(urls);
        var ajaxFunctions = {
            'success': function(result){
                var questions = result.questions;
                var answers = result.answers;
                for(let question of questions){
                    var questionObj = new Question(question.id, question.text, question.question_type, question.empty);
                    questionObj.setAnswers(answers[question.id]);
                    console.log(questionObj);
                    resultQuestions.push(questionObj);
                }
            },
            'error': function(result){
                standard.standardGetError(result);
            }
        } 
        standard.makePetition(null, 'get_questions_campaign_url', ajaxFunctions); 
        Polls.questionsList = resultQuestions;
    }

    static loadForm(result){
        Polls.campaign = result.campaign;
        Polls.call_id = result.call_id;
        Polls.header = result.header;
        Polls.agente = result.agente;
        Polls.getQuestionObjects(result.campaign);
        Polls.terceroManagement(result.terceros);
        Polls.headerManagement(result);
        Polls.drawForm();
        $('#collapsePolls').collapse('show');
        $('#anonimoInput').attr('readonly','readonly');
        $('#anonimoInput').attr('disabled','disabled');
        $('#campaignInput').attr('readonly','readonly');
        $('#campaignInput').attr('disabled','disabled');
    }

    static headerManagement(result){
        var data_llamada = result.data_llamada;
        if(data_llamada != null){
            $('#cedulaPollInput').val(data_llamada.cedula);
            $('#nombrePollInput').val(data_llamada.name);
            $('#telefonoPollInput').val(data_llamada.telefono);
            $('#correoPollInput').val(data_llamada.correo);
            $('#placaPollInput').val(data_llamada.placa);
            $('#lineaPollInput').val(data_llamada.linea_veh);
            Polls.data_llamada = data_llamada.id;
        }
    }

    static drawForm(){
        var container = $("#pollBody");
        container.empty();
        for(var i = 0; i < Polls.questionsList.length; i++){
            Polls.questionsList[i].draw(container);
        }
        $('#buttonSavePoll').removeClass('d-none');
        $('#buttonCancelPoll').removeClass('d-none');
    }

    static saveForm(){
        Polls.saveDataLlamada();
        if(Polls.checkValidity()){
            Polls.saveHeader();
            Polls.saveBodies(Polls.header);
        }
        Polls.clearDataLlamada();
        Polls.endTransaction();
    }

    static clearDataLlamada(){
        $('#telefonoPollInput').val('');
        $('#nombrePollInput').val('');
        $('#cedulaPollInput').val('');
        $('#correoPollInput').val('');
        $('#placaPollInput').val('');
        $('#lineaPollInput').val('');
        $('#campaignInput').val("");
        $('#buttonSavePoll').addClass('d-none');
        $('#buttonCancelPoll').addClass('d-none');
        Polls.data_llamada = null;
        Polls.header = null;
    }

    static saveDataLlamada(){
        var data = {};
        data['telefono'] = $('#telefonoPollInput').val();
        data['name'] = $('#nombrePollInput').val();
        data['cedula'] = $('#cedulaPollInput').val();
        data['correo'] = $('#correoPollInput').val();
        data['placa'] = $('#placaPollInput').val();
        data['linea_veh'] = $('#lineaPollInput').val();
        
        var data_llamada_id = Polls.data_llamada;
        if(data_llamada_id == null){
            Polls.addDataLlamada(data);
        }
        else {
            Polls.replaceDataLlamada(data, data_llamada_id);
        }
    }

    static addDataLlamada(data){
        var ajaxFunctions = {
            'success': function(result){
                console.log("Data llamada creado correctamente");
                Polls.data_llamada = result.id;
            },
            'error': function(result){
                SoftNotification.show("Diligencie el número de telefono del contacto");
            }
        }
        Polls.standard.makePetition(data, 'add_data_llamada_url', ajaxFunctions);
    }

    static replaceDataLlamada(data, data_llamada_id){
        var url = Polls.standard.urls['replace_data_llamada_url']['url'];
        Polls.standard.urls['replace_data_llamada_url']['url'] = url + data_llamada_id;
        var ajaxFunctions = {
            'success': function(result){
                console.log("Data llamada guardada correctamente");
            },
        }
        Polls.standard.makePetition(data, 'replace_data_llamada_url', ajaxFunctions);
        Polls.standard.urls['replace_data_llamada_url']['url'] = url;
    }

    static saveHeader(){
        var data = {};
        data['campaing'] = Polls.campaign;
        data['tercero'] = Polls.tercero;
        data['agente'] = Polls.agente;
        data['call_id'] = Polls.call_id;
        data['data_llamada'] = Polls.data_llamada;
        var header_id = Polls.header;
        if(header_id == null){
            Polls.addHeader(data);
        }
        else {
            Polls.replaceHeader(data, header_id);
        }
    }

    static saveBodies(header_id){
        var answers = {}
        var url = Polls.standard.urls['save_answers_url']['url'];
        Polls.standard.urls['save_answers_url']['url'] = url + header_id;
        for(let question of Polls.questionsList){
            var aux = question.getAnswer();
            if(Array.isArray(aux)) aux = JSON.stringify(aux);
            answers[question.id] = aux;
        }
        console.log(answers);
        var ajaxFunctions = {
            'success': function(result){
                SoftNotification.show("Respuestas guardadas correctamente");
                Polls.resetPoll();
            },
        }
        Polls.standard.makePetition(answers, 'save_answers_url', ajaxFunctions);
        Polls.standard.urls['save_answers_url']['url'] = url;
    }

    static addHeader(data){
        var ajaxFunctions = {
            'success': function(result){
                console.log("Header creado correctamente");
                Polls.header = result.id;
            },
        }
        Polls.standard.makePetition(data, 'add_header_url', ajaxFunctions);
    }

    static replaceHeader(data, header_id){
        var url = Polls.standard.urls['replace_header_url']['url'];
        Polls.standard.urls['replace_header_url']['url'] = url + header_id;
        var ajaxFunctions = {
            'success': function(result){
                console.log("Header creado correctamente");
            },
        }
        Polls.standard.makePetition(data, 'replace_header_url', ajaxFunctions);
        Polls.standard.urls['replace_header_url']['url'] = url;
    }

    static checkValidity(){
        if(Polls.data_llamada == null){
            return false;
        }
        var valid = true;
        for(let question of Polls.questionsList){
            console.log(question);
            console.log(question.isValid());
            valid = valid && question.isValid();
        }
        return valid;
    }

    static setTelefono(telefono){
        $('#telefonoPollInput').val(telefono);
    }

    static terceroManagement(terceros){
        if (terceros.length == 1){
            if (terceros[0] != null){
                $('#cedulaPollInput').val(terceros[0].nit);
                $('#nombrePollInput').val(terceros[0].nombres);
                Polls.tercero = terceros[0].nit;
            }
        }
        else if (terceros.length > 1){
            $("#selectTercero").empty();
            for(let tercero of terceros){
                $("#selectTercero").append(new Option(tercero.nombres, tercero.nit));
            }
            $('#contentTeceros').removeClass('d-none');
            $('#contentEmail').addClass('d-none');
            $('#successModal').modal('toggle');
        }
    }

    static selectTercero(){
        console.log("Yeah");
        var nombre = $( "#selectTercero option:selected").text();
        var nit = $('#selectTercero').val();
        $('#cedulaPollInput').val(nit);
        $('#nombrePollInput').val(nombre);
        $('#successModal').modal('hide');
    }

    static endTransaction(){
        AgentConsole.inTransaction = false;
    }

    static resetPoll(){
        var container = $("#pollBody");
        container.empty();
        $('#anonimoInput').removeAttr('readonly');
        $('#anonimoInput').removeAttr('disabled');
        $('#campaignInput').removeAttr('readonly');
        $('#campaignInput').removeAttr('disabled');
    }

    static cancel(){
        Polls.clearDataLlamada();
        Polls.resetPoll();
        Polls.endTransaction();
        $('#collapsePolls').collapse('hide');
    }

}


$( document ).ready(function() {

    var urlsPolls = {
        'check_tercero_cedula_url': {'url' : check_tercero_cedula_url, 'method':'POST'},
        'get_questions_campaign_url': {'url' : get_questions_campaign_url, 'method':'POST'},
        'add_header_url': {'url' : add_header_url, 'method': 'POST'},
        'replace_header_url': {'url' : replace_header_url, 'method': 'POST'},
        'save_answers_url': {'url' : save_answers_url, 'method': 'POST'},
        'add_data_llamada_url': {'url' : add_data_llamada_url, 'method': 'POST'},
        'replace_data_llamada_url': {'url' : replace_data_llamada_url, 'method': 'POST'},
    }

    Polls.standard =  new StandardCrud(urlsPolls);

    $('#campaignInput')
        .selectpicker({"liveSearch": true})
        .change(function(e){ 
            var campaign = $(e.delegateTarget).val(); 
            Polls.getQuestionObjects(campaign);
            Polls.drawForm();
            Polls.campaign = campaign;
        });

    $('#buttonSavePoll').click(Polls.saveForm);
    $('#buttonCancelPoll').click(Polls.cancel);

    $('#cedulaPollInput').change(function(){
        Polls.validateCedula();
    });

    $('#cedulaPollInput').change(function(){
        Polls.validateCedula();
    });

    $('#selectTerceroButton').click(function(){
        Polls.selectTercero();
    });

    FormFunctions.setAjaxLoadPicker('#campaignInput', picker_search_campaign_url, FormFunctions.updatePicker, "Escoja una campaña");
    FormFunctions.ajaxLoadPicker('#campaignInput', picker_search_campaign_url, FormFunctions.updatePicker, "", "Escoja una campaña");
});