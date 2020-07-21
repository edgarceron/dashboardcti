
function addFieldsNewAnswer(question){
    var html = htmlAnswer(answers);
    putAnswerHtml(html, question);
    answers++;
}

function putAnswerHtml(html, question){
    var nameContainer = "#respuestasPregunta" + question;
    var html = $(nameContainer).html() + html;
    $(nameContainer).html(html);
}

function htmlAnswer(count){
    var html =
    `
    <li class="list-group-item">
        <div class="row">
            <div class="col-md-9">
                <input type="text" class="form-control answer" id="textRespuesta${count}" value="Opcion ${count}" required>
            </div>
            <div class="col-md-2">
                <button class="btn btn-outline-primary">
                    <i class="fas fa-fw fa-save" onclick="saveAnswerButton(${count})"></i>
                </button>
            </div>
        </div>
    </li>
    `;
    return html;
}