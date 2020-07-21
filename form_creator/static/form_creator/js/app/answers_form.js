

$( document ).ready(function() {
    urls_answers = {
        'add_url': {'url' : add_answer_url, 'method':'POST'},
        'delete_url': {'url' : delete_answer_url, 'method':'DELETE'},
        'replace_url': {'url' : replace_answer_url, 'method':'PUT'}
    }
    standard_answer = new StandardCrud(urls_question);
});