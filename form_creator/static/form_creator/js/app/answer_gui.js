//TODO Tranform into a class with static method for better recognition

function addFieldsNewAnswer(questionGui, idAnswer){
    var html = htmlAnswer(answers, idAnswer, questionGui);
    putAnswerHtml(html, questionGui);
    var guiIdentifier = answers;
    answers++;
    return guiIdentifier;
}

function setDataAnswer(answer, guiIdentifier){
    var nameTextRespuesta = '#textRespuesta' + guiIdentifier;
    var htmlelement = $(nameTextRespuesta); 
    htmlelement.text(answer.text);
    htmlelement.val(answer.text);
}

function putAnswerHtml(html, question){
    var nameContainer = "#respuestasPregunta" + question;
    var html = $(nameContainer).append(html);
}

function htmlAnswer(count, idRespuesta="", questionGui=""){
    var html =
    `
    <li class="list-group-item" id="answerContainer${count}">
        <div class="row">
            <div class="col-md-9">
                <input type="text" class="form-control answer" id="textRespuesta${count}" value="Opcion ${count}" required>
                <input type="hidden" id="idRespuesta${count}" value="${idRespuesta}">
                <input type="hidden" id="idPreguntaGui${count}" value="${questionGui}">
            </div>
            <div class="col-md-1">
                <button class="btn btn-outline-primary" onclick="saveAnswer(${count})">
                    <i class="fas fa-fw fa-save"></i>
                </button>
            </div>
            <div class="col-md-1">
                <button class="btn btn-outline-primary" onclick="tryDeleteAnswer(${count})">
                    <i class="fas fa-fw fa-times"></i>
                </button>
            </div>
        </div>
    </li>
    `;
    return html;
}