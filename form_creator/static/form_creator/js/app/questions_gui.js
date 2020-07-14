/** Managges the gui elements for creating questions */
function addFieldsNewQuestion(){
    var html = htmlPregunta(questions);
    putQuestionHtml(html);
    questions++;
}

function putQuestionHtml(html){
    html = $("#questionContainer").html() + html;
    $("#questionContainer").html(html);
}

function htmlPregunta(count, idValue=""){
    var html = `
    <div class="card mt-1 mr-1 ml-1 mb-1" id="questionContainer${count}">
        <div class="card-header">
            <span>Pregunta 1</span>
            <div class="row float-right">
                <div class="col">
                    <input class="custom-control-input" onchange="questionAltered(${count})" type="checkbox" value="" id="nullPregunta${count}">
                    <label class="custom-control-label" for="nullPregunta${count}">Obligatoria</label>
                </div>
                <div class="col">
                    <button class="btn btn-outline-primary">
                        <i class="fas fa-fw fa-save" onclick="saveQuestion(${count})"></i>
                    </button>        
                </div>
                <div class="col">
                    <a href="#" onclick="tryDeleteQuestion(${count})"><i class="fas fa-fw fa-times"></i></a>
                </div>
            </div>
        </div>
        <div class="row pl-2 pb-2" id="div-pregunta${count}">
            <div class="col-md-6">
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
                </select>
                <input type="hidden" id="idPregunta${count}" value="${idValue}">
                <input type="hidden" id="alteredPregunta${count}" value="0">
            </div>
        </div>
        <div class="row pl-2 pb-2">
            <div class="col-12" id="respuestasPregunta1">
            </div>
        </div>
    </div>
    `;
    return html;
}

function showAddButtom(){
    $("#addQuetionButton").attr('disabled', false);;
}