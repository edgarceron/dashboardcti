
class AgentConsole{
    
    static call_consolidacion_id; 
    static inTransaction = false;
    static reset = false;
    static stateChanged = false;

    static getAgentState(agent, previous_state, previous_call){ 
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
                    if(result.update && !AgentConsole.inTransaction){
                        $('#lblStatus').html(result.status);
                        $('#lblMessage').html(result.message);
                        if(result.call) AgentConsole.calculateActions(result);
                        previous_state = result.previous;
                        if(result.call) previous_call = result.llamada_id;
                    }
                    if(result.update) AgentConsole.stateChanged = true;
                },
                complete: function(){
                    setTimeout(function(){ 
                        if(AgentConsole.reset){
                            AgentConsole.getAgentState(agent, -1, previous_call);
                            AgentConsole.reset = false;
                        }
                        else AgentConsole.getAgentState(agent, previous_state, previous_call);    
                    }, 1000);
                },
            });
        }
        else{
            $('#lblStatus').html("No es agente");
            $('#lblMessage').html("No hay un agente ligado a este usuario");
        }
    }

    static responseConsolidacion(result){

        data = {'data':result}
        Citas.setCallConsolidacionId(result.call_consolidacion_id);
        Citas.standard.standardSetValues(data);
    }

    static calculateActions(result){
        AgentConsole.inTransaction = true;
        var actionDecided = false;
        if (result.call_consolidacion_id){
            actionDecided = true;
            AgentConsole.responseConsolidacion(result);
        }
        else if (result.campaign){
            actionDecided = true;
            Polls.loadForm(result);
        }
        else{
            Polls.setTelefono(result.phone);
            $('#cedulaInput').val(result.cedula);
            $('#cedulaPollInput').val(result.cedula);
        }
        
    }

}


$( document ).ready(function() {
    setTimeout(function(){ 
        AgentConsole.getAgentState(id_agent, -1, "");
    }, 1000);
});
