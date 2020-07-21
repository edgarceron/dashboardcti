var questions = 1;
var answers = 1;
var urls;
var errorFields = [];
var standard;
var standard_question;
var standard_answer;
var linkedListQuestions = null;

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

$( document ).ready(function() {

    urls = {
        'listing_url': {'url': listing_url},
        'add_url': {'url' : add_url, 'method':'POST'},
        'get_url': {'url' : get_url, 'method':'POST'},
        'replace_url': {'url' : replace_url, 'method':'PUT'}
    }
    standard = new StandardCrud(urls);

    $('#nextButton').click(function(){
        saveForm();
    });

});