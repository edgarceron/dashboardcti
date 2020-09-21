//TODO Tranform into a class with static method for better recognition

function getFormDataQuestion(guiIdentifier, returnIdentifier=false){
    var nameTextPregunta = '#textPregunta' + guiIdentifier;
    var nameTypePregunta = '#typePregunta' + guiIdentifier;
    var nameNullPregunta = '#nullPregunta' + guiIdentifier;
    var namePosPregunta = '#posPregunta' + guiIdentifier;
    var nameIdPregunta = '#idPregunta' + guiIdentifier;

    $(nameTextPregunta).removeClass("is-invalid");
    data = {
        'text': $(nameTextPregunta).val(),
        'question_type': $(nameTypePregunta).val(),
        'empty': $(nameNullPregunta).is(':checked'),
        'position': $(namePosPregunta).val(),
        'form': id
    };
    if($(nameIdPregunta).val() != '') data['id'] = $(nameIdPregunta).val();
    if(returnIdentifier) data['guiIdentifier'] = guiIdentifier;
    return data;
}

function saveQuestion(guiIdentifier){
    var nameIdPregunta = '#idPregunta' + guiIdentifier;
    var nameAlteredPregunta = '#alteredPregunta' + guiIdentifier;

    var idPregunta = $(nameIdPregunta).val();
    data = getFormDataQuestion(guiIdentifier);

    if(idPregunta == "") addQuestion(data, nameIdPregunta, guiIdentifier);
    else updateQuestion(idPregunta, data, guiIdentifier);
    
    $(nameAlteredPregunta).val("0");
}

var toBeDeleted;
function deleteQuestion(idQuestion){
    raw_delete_url = standard_question.urls['delete_url'].url

    standard_question.urls['delete_url'].url = raw_delete_url + idQuestion;
    var ajaxFunctions = {
        'success': function(result){
            SoftNotification.show('Pregunta eliminada con exito');
            guiDeleteQuestion();
        }
    }
    standard_question.makePetition(null, 'delete_url', ajaxFunctions);
    standard_question.urls['delete_url'].url = raw_delete_url;
}

function tryDeleteQuestion(guiIdentifier){
    toBeDeleted = guiIdentifier;
    var nameIdPregunta = '#idPregunta' + guiIdentifier;
    idPregunta = $(nameIdPregunta).val();
    if(idPregunta == "") guiDeleteQuestion();
    else showConfirmationModal(idPregunta);
}

function showConfirmationModal(idPregunta){
    $("#confirm_button").unbind("click");
    $('#confirm_button').click(function(){
        deleteQuestion(idPregunta);
        $("#cautionModal").modal('toggle');
    });
    $("#cautionModal").modal('toggle');
    console.log("SHOW");
}

function guiDeleteQuestion(){
    var nameQuestionContainer = "#questionContainer" + toBeDeleted;
    $(nameQuestionContainer).remove();
    linkedListQuestionsDelete(toBeDeleted);
}

function saveError(request, guiIdentifier){
    var details = request.responseJSON.Error.details;
    for(field in details){
        if( details[field].field == "text") setQuestionInvalid(guiIdentifier);
    }
}

function setQuestionValidity(guiIdentifier, valid){
    var nameTextPregunta = '#textPregunta' + guiIdentifier;
    if (!valid) $(nameTextPregunta).addClass("is-invalid");
    else $(nameTextPregunta).removeClass("is-invalid");
}

function addQuestion(data, nameIdPregunta, guiIdentifier){
    var ajaxFunctions = {
        'success': function(result){
            SoftNotification.show('Pregunta guardada con exito');
            $(nameIdPregunta).val(result.id);
        },
        'error': function(request, status, error, result){
            saveError(request, guiIdentifier);
        }
    }

    standard_question.makePetition(data, 'add_url', ajaxFunctions);
}

function updateQuestion(idPregunta, data, guiIdentifier){
    raw_replace_url = standard_question.urls['replace_url'].url
    standard_question.urls['replace_url'].url = raw_replace_url + idPregunta;
    var ajaxFunctions = {
        'success': function(result){
            SoftNotification.show('Pregunta actualizada con exito');
        },
        'error': function(request, status, error, result){
            saveError(request, guiIdentifier);
        }
    }

    standard_question.makePetition(data, 'replace_url', ajaxFunctions);
    standard_question.urls['replace_url'].url = raw_replace_url;
}

function questionAltered(guiIdentifier){
    var nameAlteredPregunta = '#alteredPregunta' + guiIdentifier;
    $(nameAlteredPregunta).val("1");
    changeQuestionBehavior(guiIdentifier);
    changes = true;
}

function changeQuestionBehavior(guiIdentifier){
    var nameTypePregunta = '#typePregunta' + guiIdentifier;
    var question_type = $(nameTypePregunta).val();
    var botonOtraPregunta = '#buttonAnother' + guiIdentifier;
    if(question_type == 3 || question_type == 4){
        $(botonOtraPregunta).removeAttr("disabled");
    }
    else{
        deleteAllAnswers();
        $(botonOtraPregunta).attr("disabled","disabled");

    }
}

function isQuestionValid(guiIdentifier){
    var nameText = "#textPregunta" + guiIdentifier;
    if( $(nameText).val() != "") return true;
    return false;
}

function deleteAllAnswers(guiIdentifier){
    var nameRespuestasPregunta = '#respuestasPregunta' + guiIdentifier;
    var html = `
        <div class="col-12" id="respuestasPregunta${guiIdentifier}">
        </div>
    `;
    $(nameRespuestasPregunta).html(html);
}

function sortQuestionUp(guiIdentifier){
    linkedListQuestionsMoveUp(guiIdentifier);
    orderQuestions();
}

function sortQuestionDown(guiIdentifier){
    linkedListQuestionsMoveDown(guiIdentifier);
    orderQuestions();
}

function orderQuestions(){
    if(linkedListQuestions != null){
        var actual = linkedListQuestions;
        var container = $("#questionsContainer");
        var html  = '';
        var nameQuestionContainer;
        var nameTextPregunta;
        var nameTypePregunta;
        var nameNullPregunta;

        do {
            nameQuestionContainer = "#questionContainer" + actual.guiIdentifier;
            nameTextPregunta = '#textPregunta' + actual.guiIdentifier;
            nameTypePregunta = '#typePregunta' + actual.guiIdentifier;
            nameNullPregunta = '#nullPregunta' + actual.guiIdentifier;
            nameIdPregunta = '#idPregunta' + actual.guiIdentifier;
            idPregunta = $(nameIdPregunta).val();
            
            $(nameTextPregunta).attr('value', $(nameTextPregunta).val());
            nameTypePregunta = nameTypePregunta + " option[value='" + $(nameTypePregunta).val() + "']";

            $(nameTypePregunta).attr('selected', 'selected');
            if ($(nameNullPregunta).is(":checked")){
                $(nameNullPregunta).attr('checked', 'Yes');
            }
            $(nameQuestionContainer).find("[id^=textRespuesta]").each(
                function(){
                    $(this).attr("value", $(this).val());
                }
            );

            container.append($(nameQuestionContainer));
            actual = actual.next;
        } while (actual != null);
    }
}

$( document ).ready(function() {
    urls_question = {
        'add_url': {'url' : add_question_url, 'method':'POST'},
        'delete_url': {'url' : delete_question_url, 'method':'DELETE'},
        'replace_url': {'url' : replace_question_url, 'method':'PUT'},
        'change_question_position': {'url' : change_question_position_url, 'method':'POST'}
    }
    standard_question = new StandardCrud(urls_question);
});

