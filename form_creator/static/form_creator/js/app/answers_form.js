//TODO Tranform into a class with static method for better recognition

function getFormDataAnswer(guiIdentifier, returnIdentifier=false){
    var nameTextRespuesta = '#textRespuesta' + guiIdentifier;
    var namePreguntaGui = '#idPreguntaGui' + guiIdentifier;

    var guiPregunta = $(namePreguntaGui).val();
    var nameIdRespuesta = '#idRespuesta' + guiIdentifier;
    var nameIdPregunta = '#idPregunta' + guiPregunta;

    var idPregunta = $(nameIdPregunta).val();
    if (idPregunta == ""){
        saveQuestion(guiPregunta);
        idPregunta = $(nameIdPregunta).val();
        if(idPregunta == ""){
            SoftNotification.show("No se puede guardar la respuesta en una pregunta invalida","danger");
        }
    }

    data = {
        'text': $(nameTextRespuesta).val(),
        'question': idPregunta,
        'gui': guiIdentifier
    };
    if($(nameIdRespuesta).val() != '') data['id'] = $(nameIdRespuesta).val();
    if(returnIdentifier) data['guiIdentifier'] = guiIdentifier;
    return data;
}

function saveAnswer(guiIdentifier){
    
    var nameIdRespuesta = '#idRespuesta' + guiIdentifier;
    idRespuesta = $(nameIdRespuesta).val();

    data = getFormDataAnswer(guiIdentifier);

    if(idRespuesta == "") addAnswer(data, nameIdRespuesta);
    else updateAnswer(idRespuesta, data);
}

function addAnswer(data, nameIdRespuesta){
    var ajaxFunctions = {
        'success': function(result){
            SoftNotification.show('Pregunta guardada con exito');
            $(nameIdRespuesta).val(result.id);
        }
    }
    standard_answer.makePetition(data, 'add_url', ajaxFunctions);
}

function updateAnswer(idRespuesta, data){
    raw_replace_url = standard_answer.urls['replace_url'].url;
    standard_answer.urls['replace_url'].url = raw_replace_url + idRespuesta;
    var ajaxFunctions = {
        'success': function(result){
            SoftNotification.show('Respuesta actualizada con exito');
        }
    }

    standard_answer.makePetition(data, 'replace_url', ajaxFunctions);
    standard_answer.urls['replace_url'].url = raw_replace_url;
}

function deleteAnswer(idAnswer){
    raw_delete_url = standard_answer.urls['delete_url'].url

    standard_answer.urls['delete_url'].url = raw_delete_url + idAnswer;
    var ajaxFunctions = {
        'success': function(result){
            SoftNotification.show('Respuesta eliminada con exito');
            guiDeleteAnswer();
        }
    }
    standard_answer.makePetition(null, 'delete_url', ajaxFunctions);
    standard_answer.urls['delete_url'].url = raw_delete_url;
}

var answerToBeDeleted;
function tryDeleteAnswer(guiIdentifier){
    answerToBeDeleted = guiIdentifier;
    var nameIdRespuesta = '#idRespuesta' + guiIdentifier;
    idRespuesta = $(nameIdRespuesta).val();
    if(idRespuesta == "") guiDeleteAnswer();
    else deleteAnswer(idRespuesta);
}

function guiDeleteAnswer(){
    var nameAnswerContainer = "#answerContainer" + answerToBeDeleted;
    $(nameAnswerContainer).remove();
}

function isAnswerValid(guiIdentifier){
    var nameText = "#textRespuesta" + guiIdentifier;
    if( $(nameText).val() != "") return true;
    PollCreator.hasErrors = true;
    return false;
}

function setAnswerValidity(guiIdentifier, valid){
    var nameTextPregunta = '#textRespuesta' + guiIdentifier;
    if (!valid) $(nameTextPregunta).addClass("is-invalid");
    else $(nameTextPregunta).removeClass("is-invalid");
}

$( document ).ready(function() {
    urls_answers = {
        'add_url': {'url' : add_answer_url, 'method':'POST'},
        'delete_url': {'url' : delete_answer_url, 'method':'DELETE'},
        'replace_url': {'url' : replace_answer_url, 'method':'PUT'}
    }
    standard_answer = new StandardCrud(urls_answers);
});