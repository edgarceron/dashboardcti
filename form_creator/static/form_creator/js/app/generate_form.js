const TYPE_BOOL = 1;
const TYPE_TEXT = 2;
const TYPE_MULTI_ONE = 3;
const TYPE_MULTI_MANY = 4;

var questionList = [];


function getQuestionObjects(questions, answers){
    var ajaxFunctions = {
        'success': function(result){
            for(let question of questions){
                var questionObj = new Question(question.id, question.text, question.type, question.empty);
                questionObj.setAnswers(answers[id_queston]);
                questionList.push(questionObj);
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
        get_questions_form_url = get_questions_form_url + form_id;
    }

    urls = {
        'get_questions_form_url': {'url' : get_questions_form_url, 'method':'POST'},
    }
    standard = new StandardCrud(urls);
});