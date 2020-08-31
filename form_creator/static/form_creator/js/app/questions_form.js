
function saveQuestion(guiIdentifier){
    var nameTextPregunta = '#textPregunta' + guiIdentifier;
    var nameTypePregunta = '#typePregunta' + guiIdentifier;
    var nameNullPregunta = '#nullPregunta' + guiIdentifier;
    var nameIdPregunta = '#idPregunta' + guiIdentifier;
    var nameAlteredPregunta = '#alteredPregunta' + guiIdentifier;
    var namePosPregunta = '#posPregunta' + guiIdentifier;

    var idPregunta = $(nameIdPregunta).val();
    data = {
        'text': $(nameTextPregunta).val(),
        'question_type': $(nameTypePregunta).val(),
        'empty': $(nameNullPregunta).is(':checked'),
        'position': $(namePosPregunta).val(),
        'form': id
    };

    if(idPregunta == ""){
        addQuestion(data, nameIdPregunta);
    }
    else{
        updateQuestion(idPregunta, data);
    }
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
    if(idPregunta == ""){
        guiDeleteQuestion();
    }
    else{
        deleteQuestion(idPregunta);
    }
}

function guiDeleteQuestion(){
    var nameQuestionContainer = "#questionContainer" + toBeDeleted;
    $(nameQuestionContainer).remove();
    linkedListQuestionsDelete(toBeDeleted);
}


function addQuestion(data, nameIdPregunta){
    var ajaxFunctions = {
        'success': function(result){
            SoftNotification.show('Pregunta guardada con exito');
            $(nameIdPregunta).val(result.id);
        }
    }

    standard_question.makePetition(data, 'add_url', ajaxFunctions);
}

function updateQuestion(idPregunta, data){
    raw_replace_url = standard_question.urls['replace_url'].url
    standard_question.urls['replace_url'].url = raw_replace_url + idPregunta;
    var ajaxFunctions = {
        'success': function(result){
            SoftNotification.show('Pregunta actualizada con exito');
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
            $(nameTextPregunta).attr('value', $(nameTextPregunta).val());
            nameTypePregunta = nameTypePregunta + " option[value='" + $(nameTypePregunta).val() + "']";

            $(nameTypePregunta).attr('selected', 'selected');
            if ($(nameNullPregunta).is(":checked")){
                $(nameNullPregunta).attr('checked', 'Yes');
            }
            html = html + $(nameQuestionContainer)[0].outerHTML;
            actual = actual.next;
        } while (actual != null);

        container.html(html);
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

