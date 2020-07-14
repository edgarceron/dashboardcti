
function saveQuestion(position){
    var nameTextPregunta = '#textPregunta' + position;
    var nameTypePregunta = '#typePregunta' + position;
    var nameNullPregunta = '#nullPregunta' + position;
    var nameIdPregunta = '#idPregunta' + position;
    var nameAlteredPregunta = '#alteredPregunta' + position;

    var idPregunta = $(nameIdPregunta).val();
    data = {
        'text': $(nameTextPregunta).val(),
        'question_type': $(nameTypePregunta).val(),
        'empty': $(nameNullPregunta).val(),
        'form': id
    };

    if(idPregunta == ""){
        addQuestion(data);
    }
    else{
        updateQuestion(idPregunta, data);
    }
    $(nameAlteredPregunta).val("0");
}

function deleteQuestion(idQuestion){
    urls['delete_url'].url = urls['delete_url'].url + idQuestion;
    var ajaxFunctions = {
        'success': function(result){
            SoftNotification.show('Pregunta eliminada con exito');
        }
    }
    standard_question.makePetition(null, 'delete_url', ajaxFunctions);
}

function tryDeleteQuestion(position){
    var nameIdPregunta = '#idPregunta' + position;
    var nameQuestionContainer = "#questionContainer" + position;
    idPregunta = $(nameIdPregunta).val();
    if(idPregunta == ""){
        $(nameQuestionContainer).remove();
    }
    else{
        standard_question.standardDeleteConfirmation(idPregunta, deleteQuestion);
    }
}

function addQuestion(data){
    var ajaxFunctions = {
        'success': function(result){
            SoftNotification.show('Pregunta guardada con exito');
            question_type = ['question_type'] 
            if(question_type == 3 || question_type == 4){
                
            }
        }
    }

    standard_question.makePetition(data, 'add_url', ajaxFunctions);
}

function questionAltered(position){
    var nameAlteredPregunta = '#alteredPregunta' + position;
    $(nameAlteredPregunta).val("1");
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