//TODO Tranform into a class with static method for better recognition
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
            $("#saveAllButton").show();
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
                id_queston = question.id
                var guiIdentifier = addFieldsNewQuestion(id_queston);
                setDataQuestion(question, guiIdentifier);
                var answers_question = result.answers[id_queston];
                if(answers_question != undefined){
                    for(let answer of answers_question){
                        guiIdentifierAnswer = addFieldsNewAnswer(guiIdentifier, answer.id);
                        setDataAnswer(answer, guiIdentifierAnswer);
                    }
                }
            }
        },
        'error': function(result){
            standard.standardGetError(result);
        }
    }
    standard.makePetition(null, 'get_questions_form_url', ajaxFunctions);
}

function auxGetAll(total, name, f_check, f_get, f_set){
    var valid = true;
    var data = [];
    for (let index = 1; index < total; index++) {
        name_text = name + index;
        if($(name_text).length > 0){
            valid = f_check(index);
            if (valid) data.push(JSON.stringify(f_get(index, true)));
            f_set(index, valid);
        }
    }
    return data;
}

function getAllData(){
    var question_data = [];
    var answer_data = [];
    
    question_data = auxGetAll(
        questions, '#questionContainer', isQuestionValid,
        getFormDataQuestion, setQuestionValidity
    );

    answer_data = auxGetAll(
        answers, '#answerContainer', isAnswerValid,
        getFormDataAnswer, setAnswerValidity
    )

    data = {
        'form': JSON.stringify(getValues()),
        'questions': JSON.stringify(question_data),
        'answers': JSON.stringify(answer_data)
    }

    if (id != 0) data["id"] = id;
    return data;
}

function saveAll(){
    var ajaxFunctions = {
        'success': function(result){
            SoftNotification.show("Se guardaron todos los datos correctos");
        },
        'error': standard.standardError
    }
    standard.makePetition(getAllData(), 'save_all', ajaxFunctions);
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
        'replace_url': {'url' : replace_url, 'method':'PUT'},
        'save_all': {'url' : save_all_url, 'method':'POST'},
    }
    standard = new StandardCrud(urls);
    if(id == 0){
        $('#nextButton').click(saveForm);
        $("#saveAllButton").hide();
    }
    else{
        $('#nextButton').click(updateForm);
        $('#nextButton').html('Actualizar');
        getDataForm();
        getQuestionsForm();
        showAddButtom();
    }

    $("#saveAllButton").click(function(e){
        e.preventDefault();
        saveAll();
    });
});