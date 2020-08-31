function saveAnswer(guiIdentifier){
    var nameTextRespuesta = '#textRespuesta' + guiIdentifier;
    var nameIdPregunta = '#idPreguntaFk' + guiIdentifier;
    var nameIdRespuesta = '#idRespuesta' + guiIdentifier;
    idRespuesta = $(nameIdRespuesta).val();

    data = {
        'text': $(nameTextRespuesta).val(),
        'question': $(nameIdPregunta).val(),
    };

    if(idRespuesta == ""){
        addAnswer(data, nameIdRespuesta);
    }
    else{
        updateAnswer(idRespuesta, data);
    }
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
    raw_replace_url = standard_answer.urls['replace_url'].url
    standard_answer.urls['replace_url'].url = raw_replace_url + idRespuesta;
    var ajaxFunctions = {
        'success': function(result){
            SoftNotification.show('Respuesta actualizada con exito');
        }
    }

    standard_answer.makePetition(data, 'replace_url', ajaxFunctions);
    standard_answer.urls['replace_url'].url = raw_replace_url;
}

$( document ).ready(function() {
    urls_answers = {
        'add_url': {'url' : add_answer_url, 'method':'POST'},
        'delete_url': {'url' : delete_answer_url, 'method':'DELETE'},
        'replace_url': {'url' : replace_answer_url, 'method':'PUT'}
    }
    standard_answer = new StandardCrud(urls_answers);
});