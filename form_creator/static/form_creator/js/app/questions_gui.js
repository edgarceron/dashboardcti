/** Managges the gui elements for creating questions */
//TODO Tranform into a class with static method for better recognition

function addFieldsNewQuestion(idValue=""){
    orderQuestions();
    var html = htmlPregunta(questions, idValue);
    putQuestionHtml(html);
    linkedQuestionListAdd(questions);
    guiIdentifier = questions;
    questions++;
    return guiIdentifier;
}

function setDataQuestion(question, guiIdentifier){
    var nameTextPregunta = '#textPregunta' + guiIdentifier;
    var nameTypePregunta = '#typePregunta' + guiIdentifier;
    var nameNullPregunta = '#nullPregunta' + guiIdentifier;
    var namePosPregunta = '#posPregunta' + guiIdentifier;
    
    $(nameTextPregunta).val(question.text);
    $(nameTypePregunta).val(question.question_type);
    $(nameTypePregunta).val(question.question_type);
    if(question.empty) {
        $(nameNullPregunta).prop('checked', 'checked');
    }
    
    $(namePosPregunta).val(question.position);

    changeQuestionBehavior(guiIdentifier);
}

function putQuestionHtml(html){
    html = $("#questionsContainer").html() + html;
    $("#questionsContainer").html(html);
}

function htmlPregunta(count, idValue=""){
    var html = `
    <div class="card mt-1 mr-1 ml-1 mb-1" id="questionContainer${count}">
        <div class="card-header">
            <span>Pregunta ${count}</span>
            <div class="row float-right">
                <div class="col">
                    <input class="custom-control-input" onchange="questionAltered(${count})" type="checkbox" value="" id="nullPregunta${count}">
                    <label class="custom-control-label" for="nullPregunta${count}">Obligatoria</label>
                </div>
                <div class="col btn-group btn-group-toggle">
                    <button type="button" class="btn btn-primary" onclick="sortQuestionDown(${count})">
                        <i class="fas fa-chevron-down"></i>
                    </button>
                    <button type="button" class="btn btn-primary" onclick="sortQuestionUp(${count})">
                        <i class="fas fa-chevron-up"></i>
                    </button> 
                </div>
                <div class="col">
                    <button class="btn btn-outline-primary" onclick="saveQuestion(${count})">
                        <i class="fas fa-fw fa-save"></i>
                    </button>        
                </div>
                <div class="col">
                    <button class="btn btn-outline-primary" onclick="tryDeleteQuestion(${count})">
                        <i class="fas fa-fw fa-times"></i>
                    </button>   
                </div>
            </div>
        </div>
        <div class="row pl-2 pb-2" id="div-pregunta${count}">
            <div class="col-md-7">
                <label for="textPregunta${count}">Pregunta</label>
                <input type="text" class="form-control" onkeydown="questionAltered(${count})" id="textPregunta${count}" required>
            </div>
            <div class="col-md-4">
                <label for="typePregunta${count}">Tipo</label>
                <select class="form-control" onchange="questionAltered(${count})" id="typePregunta${count}">
                    <option value="1">Falso o verdadero</option>
                    <option value="2">Texto</option>
                    <option value="3">Multiples opciones, una respuesta</option>
                    <option value="4">Multiples opciones, multiples respuestas</option>
                    <option value="5">Fecha y hora</option>
                </select>
                <input type="hidden" id="idPregunta${count}" value="${idValue}">
                <input type="hidden" id="alteredPregunta${count}" value="0">
                <input type="hidden" id="posPregunta${count}" value="${count}">
            </div>
        </div>
        <div class="row pl-2 pb-2">
            <div class="col-12" id="respuestasPregunta${count}">
            </div>
        </div>
        <div class="row pl-2 pb-2" id=>
            <div class="col-12">
                <ul class="list-group list-group-flush">
                    <li class="list-group-item">
                        <button type="button" class="btn btn-primary" onclick="addFieldsNewAnswer(${count})" disabled="disabled" id="buttonAnother${count}">Otra respuesta</button>
                    </li>
                </ul>
            </div>
        </div>
    </div>
    `;
    return html;
}

function showAddButtom(){
    $("#addQuetionButton").attr('disabled', false);;
}