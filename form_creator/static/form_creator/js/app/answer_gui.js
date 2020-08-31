
function addFieldsNewAnswer(question){
    var nameIdPregunta = '#idPregunta' + question;
    var idPregunta = $(nameIdPregunta).val();
    var html = htmlAnswer(answers, idPregunta);
    putAnswerHtml(html, question);
    answers++;
}

function putAnswerHtml(html, question){
    var nameContainer = "#respuestasPregunta" + question;
    var html = $(nameContainer).html() + html;
    $(nameContainer).html(html);
}

function htmlAnswer(count, idPregunta, idRespuesta=""){
    var html =
    `
    <li class="list-group-item">
        <div class="row">
            <div class="col-md-9">
                <input type="text" class="form-control answer" id="textRespuesta${count}" value="Opcion ${count}" required>
                <input type="hidden" id="idRespuesta${count}" value="${idRespuesta}">
                <input type="hidden" id="idPreguntaFk${count}" value="${idPregunta}">
            </div>
            <div class="col-md-2">
                <button class="btn btn-outline-primary">
                    <i class="fas fa-fw fa-save" onclick="saveAnswer(${count})"></i>
                </button>
            </div>
        </div>
    </li>
    `;
    return html;
}