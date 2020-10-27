var call_consolidacion_id; 
var inTransaction = false;
var reset = false;
var stateChanged = false;

function getAgentState(agent, previous_state, previous_call){ 
    if(agent != null){
        $.ajax({
            url: agent_state_url,
            method: 'POST',
            async: true,
            dataType: 'json',
            data: {
                'id_agent': agent,
                'previous_state':previous_state,
                'previous_call':previous_call
            },
            success: function(result){
                if(result.update && !inTransaction){
                    $('#lblStatus').html(result.status);
                    $('#lblMessage').html(result.message);
                    if(result.call) calculateActions(result);
                    previous_state = result.previous;
                    if(result.call) previous_call = result.llamada_id;
                }
                if(result.update) stateChanged = true;
            },
            complete: function(){
                setTimeout(function(){ 
                    if(reset){
                        getAgentState(agent, -1, previous_call);
                        reset = false;
                    }
                    else getAgentState(agent, previous_state, previous_call);    
                }, 1000);
            },
        });
    }
    else{
        $('#lblStatus').html("No es agente");
        $('#lblMessage').html("No hay un agente ligado a este usuario");
    }
}

function responseConsolidacion(result){
    $('#contentCita').removeClass('d-none');
    $('#contentEmail').addClass('d-none');
    $('#fechaInput').val("");
    $('#successModal').modal('show');
    $('#successModal').modal({backdrop:'static', keyboard:false});

    data = {'data':result}
    Citas.setCallConsolidacionId(result.call_consolidacion_id);
    StandardCrud.standardSetValues(data);
}

function calculateActions(result){
    inTransaction = true;
    var actionDecided = false;
    if (result.call_consolidacion_id){
        actionDecided = true;
        responseConsolidacion(result);
    }
    else if (result.campaign){
        actionDecided = true;
        Polls.loadForm(result);
    }
    Polls.setTelefono(result.phone);
}


$( document ).ready(function() {
    setTimeout(function(){ 
        getAgentState(id_agent, -1, "");
    }, 1000);
});
