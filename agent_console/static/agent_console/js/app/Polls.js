class Polls {
    static standard = null;
    static validateCedula(){
        var ajaxFunctions = {
            'success': function(result){
                if(result.success){
                    $('#nombrePollInput').val(result.nombre);
                }
                else {
                    SoftNotification.show(result.message);
                }
            },
            'error': standard.standardError
        }
        standard.makePetition(getValues(), 'validate_cedula_url', ajaxFunctions);
    }

    static getQuestionObjects(form_id){
        var questionList = [];
        var urls = {
            'get_questions_form_url': {'url' : get_questions_form_url + form_id, 'method':'POST'},
        }
        var standard = new StandardCrud(urls);
        var ajaxFunctions = {
            'success': function(result){
                var questions = result.questions;
                var answers = result.answers;
                for(let question of questions){
                    var questionObj = new Question(question.id, question.text, question.type, question.empty);
                    questionObj.setAnswers(answers[question.id]);
                    questionList.push(questionObj);
                }
            },
            'error': function(result){
                standard.standardGetError(result);
            }
        } 
        standard.makePetition(null, 'get_questions_form_url', ajaxFunctions); 
        return questionList;   
    }
}


$( document ).ready(function() {

    var urlsPolls = {
        'validate_cedula_url': {'url' : validate_cedula_url, 'method':'POST'},
        'get_questions_form_url': {'url' : get_questions_form_url, 'method':'POST'},
    }

    Polls.standard =  new StandardCrud(urlsPolls);

    $('#campaignInput').selectpicker(
        {
            "liveSearch": true
        }
    );

    FormFunctions.setAjaxLoadPicker('#campaignInput', picker_search_campaign_url, FormFunctions.updatePicker, "Escoja una campaña");
    FormFunctions.ajaxLoadPicker('#campaignInput', picker_search_campaign_url, FormFunctions.updatePicker, "", "Escoja una campaña");
});