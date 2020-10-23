class Polls {
    static standard = null;
    static questionsList = [];
    static terceroValid = false;
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
                    SoftNotification.show("No existe un cliente con esta cedula");
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
        Polls.getQuestionObjects(result.campaign);
        Polls.terceroManagement(result.terceros);
        Polls.drawForm();
    }

    static drawForm(){
        var container = $("#pollBody");
        container.empty();
        for(var i = 0; i < Polls.questionsList.length; i++){
            Polls.questionsList[i].draw(container);
        }
        $('#buttonSavePoll').removeClass('d-none')
    }

    static saveForm(){
        if(Polls.checkValidity()){
            //saveHeader();
            //saveBody();
        }
    }

    static saveHeader(){
        
    }

    static checkValidity(){
        var valid = true;
        for(let question of Polls.questionsList){
            console.log(question);
            console.log(question.isValid());
            valid = valid && question.isValid();
        }
        Polls.validateCedula();
        return valid && Polls.terceroValid;
    }

    static terceroManagement(terceros){
        if (terceros.length == 1){
            $('#cedulaPollInput').val(terceros[0].nit);
            $('#nombrePollInput').val(terceros[0].nombres);
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

}


$( document ).ready(function() {

    var urlsPolls = {
        'check_tercero_cedula_url': {'url' : check_tercero_cedula_url, 'method':'POST'},
        'get_questions_campaign_url': {'url' : get_questions_campaign_url, 'method':'POST'},
    }

    Polls.standard =  new StandardCrud(urlsPolls);

    $('#campaignInput')
        .selectpicker({"liveSearch": true})
        .change(function(e){ 
            var campaign = $(e.delegateTarget).val(); 
            Polls.getQuestionObjects(campaign);
            Polls.drawForm();
        });

    $('#buttonSavePoll').click(function(){
        Polls.saveForm();
    });

    FormFunctions.setAjaxLoadPicker('#campaignInput', picker_search_campaign_url, FormFunctions.updatePicker, "Escoja una campaña");
    FormFunctions.ajaxLoadPicker('#campaignInput', picker_search_campaign_url, FormFunctions.updatePicker, "", "Escoja una campaña");
});