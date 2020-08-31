
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
        console.log(actual);
        if(actual.guiIdentifier != guiIdentifier){
            before = actual;
            actual = actual.next;
        }
        else{
            before.next = actual.next;
            break;
        }
    }while (actual != null);
    reCalculatePositions();
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
        reCalculatePositions();   
    }
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
        reCalculatePositions();
    }
}

function reCalculatePositions(){
    var actual = linkedListQuestions;
    var pos = 1;
    var namePosPregunta = "";
    while(actual != null){
        namePosPregunta = "#posPregunta" + actual.guiIdentifier;
        $(namePosPregunta).val(pos);
        pos++;
        actual = actual.next;
    }
}