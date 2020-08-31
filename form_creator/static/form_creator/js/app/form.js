var questions = 1;
var answers = 1;
var urls;
var errorFields = [];
var standard;
var standard_question;
var standard_answer;
var linkedListQuestions = null;
var changes = false;

function getValues(){
    data = {
        'name': $('#nameInput').val()
    }
    return data;
}

function saveForm(){
    var ajaxFunctions = {
        'success': function(result){
            FormFunctions.resetFormErrors(errorFields);
            errorFields = [];
            SoftNotification.show("Creado, por favor agregue preguntas al formulario");
            id = result.id;
            addFieldsNewQuestion();
            showAddButtom();
            urls['replace_url'].url = urls['replace_url'].url + id;
            standard = new StandardCrud(urls);
            $('#nextButton').unbind("click");
            $('#nextButton').click(function(){
                updateForm();
            });
            $('#nextButton').html('Actualizar');
        },
        'error': standard.standardError
    }
    standard.makePetition(getValues(), 'add_url', ajaxFunctions);
}

function updateForm(){
    var ajaxFunctions = {
        'success': function(result){
            FormFunctions.resetFormErrors(this.errorFields);
            this.errorFields = [];
            SoftNotification.show("Formulario actualizado");
            id = result.id;
        },
        'error': standard.standardError
    }
    standard.makePetition(getValues(), 'replace_url', ajaxFunctions);
}

function getDataForm(){
    var ajaxFunctions = {
        'success': function(result){
            standard.standardSetValues(result);
        },
        'error': function(result){
            standard.standardGetError(result);
        }
    }
    standard.makePetition(null, 'get_url', ajaxFunctions);
}

function getQuestionsForm(){
    var ajaxFunctions = {
        'success': function(result){
            for(let question of result.questions){
                guiIdentifier = addFieldsNewQuestion(question.id);
                setDataQuestion(question, guiIdentifier);
            }
        },
        'error': function(result){
            standard.standardGetError(result);
        }
    }
    standard.makePetition(null, 'get_questions_form_url', ajaxFunctions);
}

$( document ).ready(function() {

    if(id != 0){
        get_url = get_url + id;
        get_questions_form_url = get_questions_form_url + id;
        replace_url = replace_url + id;
    }

    urls = {
        'listing_url': {'url': listing_url},
        'add_url': {'url' : add_url, 'method':'POST'},
        'get_url': {'url' : get_url, 'method':'POST'},
        'get_questions_form_url': {'url' : get_questions_form_url, 'method':'POST'},
        'replace_url': {'url' : replace_url, 'method':'PUT'}
    }
    standard = new StandardCrud(urls);

    if(id == 0){
        getDataForm();
        $('#nextButton').click(function(){
            saveForm();
        });
    }
    else{
        $('#nextButton').click(function(){
            updateForm();
        });
        $('#nextButton').html('Actualizar');
    }

    if(id!=0){
        getDataForm();
        getQuestionsForm();
        showAddButtom();
    }

});