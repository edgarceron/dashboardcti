
function saveQuestion(guiIdentifier){
    var nameTextPregunta = '#textPregunta' + guiIdentifier;
    var nameTypePregunta = '#typePregunta' + guiIdentifier;
    var nameNullPregunta = '#nullPregunta' + guiIdentifier;
    var nameIdPregunta = '#idPregunta' + guiIdentifier;
    var nameAlteredPregunta = '#alteredPregunta' + guiIdentifier;

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

var toBeDeleted;
function deleteQuestion(idQuestion){
    urls['delete_url'].url = urls['delete_url'].url + idQuestion;
    var ajaxFunctions = {
        'success': function(result){
            SoftNotification.show('Pregunta eliminada con exito');
            guiDeleteQuestion();
        }
    }
    standard_question.makePetition(null, 'delete_url', ajaxFunctions);
}

function tryDeleteQuestion(guiIdentifier){
    toBeDeleted = guiIdentifier;
    var nameIdPregunta = '#idPregunta' + guiIdentifier;
    idPregunta = $(nameIdPregunta).val();
    if(idPregunta == ""){
        guiDeleteQuestion();
    }
    else{
        standard_question.standardDeleteConfirmation(idPregunta, deleteQuestion);
    }
}

function guiDeleteQuestion(){
    var nameQuestionContainer = "#questionContainer" + toBeDeleted;
    $(nameQuestionContainer).remove();
    linkedListQuestionsDelete(toBeDeleted);
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

function questionAltered(guiIdentifier){
    var nameAlteredPregunta = '#alteredPregunta' + guiIdentifier;
    $(nameAlteredPregunta).val("1");
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
        var namePosPregunta;

        do {
            var nameQuestionContainer = "#questionContainer" + actual.guiIdentifier;
            var nameTextPregunta = '#textPregunta' + actual.guiIdentifier;
            var nameTypePregunta = '#typePregunta' + actual.guiIdentifier;
            var nameNullPregunta = '#nullPregunta' + actual.guiIdentifier;
            $(nameTextPregunta).attr('value', $(nameTextPregunta).val());
            nameTypePregunta = nameTypePregunta + " option[value='" + $(nameTypePregunta).val() + "']";
            console.log(nameTypePregunta);
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

