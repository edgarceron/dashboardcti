
function linkedQuestionListAdd(guiIdentifier){
    var pos = 1;
    if(linkedListQuestions == null){
        linkedListQuestions = {'guiIdentifier': guiIdentifier, 'next': null};
    }
    else{
        var actual = linkedListQuestions;
        do{
            pos++;
            next = actual.next;
            if(next != null){
                actual = next;
            }
        } while(next != null);
        actual.next = {'guiIdentifier': guiIdentifier, 'next': null}
    }
    namePosPregunta = "#posPregunta" + guiIdentifier;
    $(namePosPregunta).val(pos);
    console.log(linkedListQuestions);
}

function linkedListQuestionsDelete(guiIdentifier){
    var before = null;
    var actual = linkedListQuestions;
    do {
        if(actual.guiIdentifier != guiIdentifier){
            before = actual;
            actual = actual.next;
        }
    }while (actual.guiIdentifier != guiIdentifier && actual != null);

    if(before != null){
        before.next = recursivePosChange(actual.next);
    }
    else{
        linkedListQuestions = null;
    }
    console.log(linkedListQuestions);
}

function recursivePosChange(linked){
    if(linked == null){
        return null;
    }
    guiIdentifier == linked.guiIdentifier;
    moveToRelativePosition(guiIdentifier, -1);
    linked.next = recursivePosChange(linked.next);
    return linked;
}

function linkedListQuestionsMoveUp(guiIdentifier){
    actual = linkedListQuestions;
    before = null;
    
    do {
        if(actual.guiIdentifier != guiIdentifier){
            before = actual;
            actual = actual.next;
        }
    }while (actual.guiIdentifier != guiIdentifier && actual != null);

    if(before != null){
        var aux = before.guiIdentifier;
        before.guiIdentifier = actual.guiIdentifier;
        actual.guiIdentifier = aux; 
        moveToRelativePosition(actual.guiIdentifier, -1);
        moveToRelativePosition(before.guiIdentifier, 1);     
    }
    console.log(linkedListQuestions);
}

function linkedListQuestionsMoveDown(guiIdentifier){
    actual = linkedListQuestions;
    do {
        if(actual.guiIdentifier != guiIdentifier){
            actual = actual.next;
        }
    }while (actual.guiIdentifier != guiIdentifier && actual != null);

    next = actual.next;
    if(next != null){
        var aux = next.guiIdentifier;
        next.guiIdentifier = actual.guiIdentifier;
        actual.guiIdentifier = aux;
        moveToRelativePosition(actual.guiIdentifier, 1);
        moveToRelativePosition(next.guiIdentifier, -1);        
    }
    console.log(linkedListQuestions);
}

function moveToRelativePosition(guiIdentifier, distance){
    namePosPregunta = "#posPregunta" + guiIdentifier;
    posPreguntaInput = $(namePosPregunta);
    posPreguntaInput.val( parseInt(posPreguntaInput.val()) + distance);
}