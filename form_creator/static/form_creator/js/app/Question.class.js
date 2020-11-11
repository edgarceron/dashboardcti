class Question {

    static TYPE_BOOL = 1;
    static TYPE_TEXT = 2;
    static TYPE_MULTI_ONE = 3;
    static TYPE_MULTI_MANY = 4;
    static TYPE_DATE = 5;

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

    setValidation(){
        var selector;
        if(this.type == Question.TYPE_BOOL){
            selector = `#checkPregunta${this.id}`;
        }
        else if (this.type == Question.TYPE_TEXT){
            selector = `#textAreaPregunta${this.id}`;
        }
        else if (this.type == Question.TYPE_MULTI_ONE){
            selector = `[id$=pregunta${this.id}]`;
        }
        else if (this.type == Question.TYPE_MULTI_MANY){
            selector = `[id$=pregunta${this.id}]`;
        }
        else if (this.type == Question.TYPE_DATE){
            selector = `#datePregunta${this.id}`;
        }
        console.log($(selector));
        if(!this.isValid()) $(selector).addClass('is-invalid');
        else $(selector).removeClass('is-invalid');
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
        else if (this.type == Question.TYPE_DATE){
            html = this.drawDate();
        }
        container.html(container.html() + html);

        var selector = ".form_datetime"
        jQuery(selector).datetimepicker({
            allowTimes:[
                '7:00', '7:15', '7:30', '7:45', 
                '8:00', '8:15', '8:30', '8:45', 
                '9:00', '9:15', '9:30', '9:45', 
                '10:00', '10:15', '10:30', '10:45', 
                '11:00', '11:15', '11:30', '11:45', 
                '12:00', '12:15', '12:30', '12:45', 
                '13:00', '13:15', '13:30', '13:45', 
                '14:00', '14:15', '14:30', '14:45', 
                '15:00', '15:15', '15:30', '15:45', 
                '16:00', '16:15', '16:30', '16:45', 
            ]
        });
    }

    drawBool(){
        var required = this.empty ? "required" : "";
        var ast = this.empty ? "*" : "";
        var html = `
            <div class="row">
                <div class="col-md-11">
                    <div class="row">
                        <div class="col-md-12" id="checkPregunta${this.id}">     
                            ${this.text}${ast}
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
        var required = this.empty ? "required" : "";
        var ast = this.empty ? "*" : "";
        var html = `
            <div class="row">
                <div class="col-md-12">
                    ${this.text} ${ast}
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
        var ast = this.empty ? "*" : "";
        var html = `
        <div class="row">
            <div class="col-md-12">
                ${this.text}${ast}
        `;
        var answer;
        for(var i = 0; i < this.answers.length; i++){
            answer = this.answers[i];
            var answerHtml = `
            <div class="form-check">
            <input 
                class="form-check-input" type="radio" 
                name="pregunta${this.id}" id="respuesta${answer.id}pregunta${this.id}" 
                value="${answer.id}">
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
        var ast = this.empty ? "*" : "";
        var html = `
        <div class="row">
            <div class="col-md-12">
                ${this.text}${ast}
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

    drawDate(){
        var ast = this.empty ? "*" : "";
        var required = this.empty ? "required" : "";
        var html = `
            <div class="row">
                <div class="col-md-12">
                    ${this.text}${ast}
                    <div class="form-group">
                        <input type="text" class="form-control form_datetime" id="datePregunta${this.id}" ${required}>
                    </div>
                </div>
            </div>
        `;
        var selector = `#datePregunta${this.id}`;
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
            case Question.TYPE_DATE:
                    name = "#datePregunta" + this.id;
                    var input = $(name);
                    if (this.empty){
                        if(input.val().trim() != "") return true;
                        return false;
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
            case Question.TYPE_DATE:
                name = "#datePregunta" + this.id;
                return $(name).val();
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
