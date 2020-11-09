
class AgentConsole{
    
    static call_consolidacion_id; 
    static inTransaction = false;
    static reset = false;
    static stateChanged = false;
    static since = 0;
    static limit_break = 0;
    static break = "";
    static llamada_id = 0;

    static getAgentState(agent, previous_state, previous_call, previous_break){ 
        if(agent != null){
            $.ajax({
                url: agent_state_url,
                method: 'POST',
                async: true,
                dataType: 'json',
                data: {
                    'id_agent': agent,
                    'previous_state':previous_state,
                    'previous_call':previous_call,
                    'previous_break':previous_break
                },
                success: function(result){
                    if(result.update && !AgentConsole.inTransaction){
                        $('#lblStatus').html(result.status);
                        $('#lblMessage').html(result.message);
                        if(result.call) AgentConsole.calculateActions(result);
                        if(result.break != ""){
                            AgentConsole.since = new Date(result.date + " " + result.time);
                            AgentConsole.break = result.break;
                            AgentConsole.limit_break = result.time_limit;
                        }
                        else AgentConsole.since = 0;
                        previous_break = result.break;
                        previous_state = result.previous;
                        if(result.call) {
                            previous_call = result.llamada_id;
                            AgentConsole.llamada_id = result.llamada_id;
                        };
                    }
                    if(result.update) AgentConsole.stateChanged = true;
                },
                complete: function(){
                    setTimeout(function(){ 
                        if(AgentConsole.reset){
                            AgentConsole.getAgentState(agent, -1, previous_call, previous_break);
                            AgentConsole.reset = false;
                        }
                        else AgentConsole.getAgentState(agent, previous_state, previous_call, previous_break);    
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
        var data = {'data':result}
        Citas.setCallConsolidacionId(result.call_consolidacion_id);
        Citas.standard.standardSetValues(data);
        $('#collapseCitas').collapse('show');
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

    static msToTime(duration) {
        var milliseconds = parseInt((duration % 1000) / 100),
          seconds = Math.floor((duration / 1000) % 60),
          minutes = Math.floor((duration / (1000 * 60)) % 60),
          hours = Math.floor((duration / (1000 * 60 * 60)) % 24);
      
        hours = (hours < 10) ? "0" + hours : hours;
        minutes = (minutes < 10) ? "0" + minutes : minutes;
        seconds = (seconds < 10) ? "0" + seconds : seconds;
      
        return hours + ":" + minutes + ":" + seconds;
    }

    static checkAlerta(duration, limit){
        var seconds = Math.floor(duration / 1000);
        var remaining_time = limit - seconds;
        if(remaining_time < 0){
            SoftNotification.show("El tiempo permitido para el descanso ha terminado","danger");
        }
        else if (remaining_time < 60){
            SoftNotification.show("Queda menos de un minuto para terminar el descanso","warning");
        }
    }

    static setTimeBreak(){
        if(AgentConsole.since != 0){
            var time = Math.abs(new Date() - AgentConsole.since);
            $('#lblStatus').html("En descanso: " + AgentConsole.break);
            $('#lblMessage').html("Tiempo: " + AgentConsole.msToTime(time));
        }
    }

    static setAlertBreak(){
        if(AgentConsole.since != 0){
            var time = Math.abs(new Date() - AgentConsole.since);
            AgentConsole.checkAlerta(time, AgentConsole.limit_break);
        }
    }
}




$( document ).ready(function() {
    setTimeout(function(){ 
        AgentConsole.getAgentState(id_agent, -1, "", "");
    }, 1000);

    setInterval(function(){
        AgentConsole.setTimeBreak();
    }, 1000)

    setInterval(function(){
        AgentConsole.setAlertBreak();
    }, 15000)
});
