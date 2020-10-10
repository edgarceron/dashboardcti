class Question {

    constructor(id, text, type, empty){
        this.text = text;
        this.type = type;
        this.empty = empty;
        this.id = id;
        this.answers = [];
    }

    setAnswers(answers){
        this.answers = answers;
    }

    draw(container){
        var html;
        if(this.type == TYPE_BOOL){
            html = this.drawBool();
        }
        else if (this.type == TYPE_TEXT){
            html = this.drawText();
        }
        else if (this.type == TYPE_MULTI_ONE){
            html = this.drawMultiOne();
        }
        else if (this.type == TYPE_MULTI_MANY){
            html = this.drawMultiMany();
        }
        container.html(container.html() + html);
    }

    drawBool(){
        var required = this.empty ? "" : "required";
        var html = `
            <div class="row">
                <div class="col-md-11">
                    <div class="row">
                        <div class="col-md-12">     
                            ${this.text}
                        </div>
                    </div>
                </div>
                <div class="col-md-1">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="1" id="checkPregunta${this.id}" ${required}>
                    </div>
                </div>
            </div>
        `
        return this.cardEnvelope(html);
    }

    drawText(){
        var required = this.empty ? "" : "required";
        var html = `
            <div class="row">
                <div class="col-md-12">
                    ${this.text}
                    <div class="form-group">
                        <textarea class="form-control" id="textAreaPregunta${this.id}" rows="3" ${required}>
                        </textarea>
                    </div>
                </div>
            </div>
        `;
        return this.cardEnvelope(html);
    }

    drawMultiOne(){
        var html = `
        <div class="row">
            <div class="col-md-12">
                ${this.text}
        `;

        var answer;
        for(var i = 0; i < this.answers.length; i++){
            answer = this.answers[i];
            var answerHtml = `
            <div class="form-check">
            <input 
                class="form-check-input" type="radio" 
                name="pregunta${this.id}" id="respuesta${answer.id}pregunta${this.id}" 
                value="${this.id}">
            <label class="form-check-label" for="respuesta${answer.id}pregunta${this.id}">
                ${answer.text}
            </label>
            </div>
            `;
            html += answerHtml;
        }

        html += `
            </div>
        </div>
        `;
        return cardEnvelope(html);
    }

    drawMultiMany(){
        var html = `
        <div class="row">
            <div class="col-md-12">
                ${this.text}
        `;

        var answer;
        for(var i = 0; i < this.answers.length; i++){
            answer = this.answers[i];
            var answerHtml = `
            <div class="col-md-12">
                <div class="form-check">
                    <input 
                        class="form-check-input" name="pregunta${this.id}" type="checkbox" 
                        value="${answer.id}" id="respuesta${answer.id}pregunta${this.id}">
                    <label class="form-check-label" for="respuesta${answer.id}pregunta${this.id}">
                        ${answer.text}
                    </label>
                </div>
            </div>
            `;
            html += answerHtml;
        }

        html += `
            </div>
        </div>
        `;

        return cardEnvelope(html);
    }

    isValid(){
        var name = "";
        var idPregunta;
        var selector;
        switch (this.type){
            case TYPE_BOOL:
                return true;
            case TYPE_TEXT:
                name = "#textAreaPregunta" + this.id;
                var input = $(name);
                if (this.required){
                    if(input.text().trim() != "") return true;
                    return false;
                }
                return true;
            case TYPE_MULTI_ONE:
                idPregunta = "pregunta" + this.id;
                selector = '[id$='+ idPregunta +'] :checked';
                if(this.required && $(selector).length == 1) return true;
                return false;
            case TYPE_MULTI_MANY:
                idPregunta = "pregunta" + this.id;
                selector = '[id$='+ idPregunta +'] :checked';
                if (this.required){
                    if($(selector).length >= 1) return true;
                    return false;
                }
                return true;
        }
    }

    getAnswer(){
        var name = "";
        switch (this.type){       
            case TYPE_BOOL:
                name = "#checkPregunta" + this.id;
                return $(name).prop('checked');
            case TYPE_TEXT:
                name = "#textAreaPregunta" + this.id;
                return $(name).text();
            case TYPE_MULTI_ONE:
                idPregunta = "pregunta" + this.id;
                selector = '[id$='+ idPregunta +'] :checked';
                var selected = $(selector);
                if(selected.length == 0) return [];
                return $(selector).val();
            case TYPE_MULTI_MANY:
                idPregunta = "pregunta" + this.id;
                selector = '[id$='+ idPregunta +'] :checked';
                var selected = $(selector);
                if(selected.length == 0) return [];
                else if(selected.length == 1)  return $(selector).val();
                else {
                    var values = []
                    for(var i = 0; i < selected.length; i++){
                        values.push(selected[i].val());
                    }
                    return values;
                }
        }
    }

    cardEnvelope(html){
        html = `
        <div class="card w-100">
            <div class="card-body">` + 
            html + `
            </div>
        </div>
        ` 
        return html;
    }
}