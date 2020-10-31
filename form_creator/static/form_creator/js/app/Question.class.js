class Question {

    static TYPE_BOOL = 1;
    static TYPE_TEXT = 2;
    static TYPE_MULTI_ONE = 3;
    static TYPE_MULTI_MANY = 4;

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
        if(this.type == Question.TYPE_BOOL){
            html = this.drawBool();
        }
        else if (this.type == Question.TYPE_TEXT){
            html = this.drawText();
        }
        else if (this.type == Question.TYPE_MULTI_ONE){
            html = this.drawMultiOne();
        }
        else if (this.type == Question.TYPE_MULTI_MANY){
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
        return this.cardEnvelope(html);
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

        return this.cardEnvelope(html);
    }

    isValid(){
        var name = "";
        var idPregunta;
        var selector;
        switch (this.type){
            case Question.TYPE_BOOL:
                return true;
            case Question.TYPE_TEXT:
                name = "#textAreaPregunta" + this.id;
                var input = $(name);
                if (this.empty){
                    if(input.val().trim() != "") return true;
                    return false;
                }
                return true;
            case Question.TYPE_MULTI_ONE:
                idPregunta = "pregunta" + this.id;
                selector = '[id$='+ idPregunta +']';
                var checked = false;
                $(selector).each(
                    function(){
                        checked = checked || $(this).is(":checked");
                    }
                );
                return checked;
            case Question.TYPE_MULTI_MANY:
                idPregunta = "pregunta" + this.id;
                selector = '[id$='+ idPregunta +']';
                if (this.empty){
                    var checked = false;
                    $(selector).each(
                        function(){
                            checked = checked || $(this).is(":checked");
                        }
                    );
                    return checked;
                }
                return true;
        }
    }

    getAnswer(){
        var name = "";
        switch (this.type){       
            case Question.TYPE_BOOL:
                name = "#checkPregunta" + this.id;
                return $(name).prop('checked');
            case Question.TYPE_TEXT:
                name = "#textAreaPregunta" + this.id;
                return $(name).val();
            case Question.TYPE_MULTI_ONE:
                var idPregunta = "pregunta" + this.id;
                var selector = '[id$='+ idPregunta +']';
                var checked;
                $(selector).each(
                    function(){
                        if($(this).is(":checked")){
                            checked = $(this).val();
                        }
                    }
                );
                return checked;
            case Question.TYPE_MULTI_MANY:
                var idPregunta = "pregunta" + this.id;
                var selector = '[id$='+ idPregunta +']';
                var selected = [];
                $(selector).each(
                    function(){
                        if($(this).is(":checked")){
                            selected.push($(this).val());
                        }
                    }
                );
                return selected;
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