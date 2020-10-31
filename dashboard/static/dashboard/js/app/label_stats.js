function setStatsLabels(callEntryCount){
    $("#lblTotal").html(callEntryCount["total"]);
    $("#lblTerminadas").html(callEntryCount["terminada"]);
    $("#lblAbandonadas").html(callEntryCount["abandonada"]);
    $("#lblCola").html(callEntryCount["en-cola"]);
    $("#lblBefore").html(callEntryCount["before"]);
}

function setStatsAgents(agents_logged, agents_in_break, agents_in_call){
    $("#lblLogged").html(agents_logged);
    $("#lblBreak").html(agents_in_break);
    $("#lblIncall").html(agents_in_call);
}

function setStatsLabelsOut(callsCount){
    var pendientes = callsCount["Placing"] + callsCount[null];
    var fallidas = callsCount["Abandoned"] + callsCount["Failure"] + callsCount["ShortCall"] + callsCount["NoAsnwer"];
    $("#lblTotalOut").html(callsCount["total"]);
    $("#lblTerminadasOut").html(callsCount["Success"]);
    $("#lblFallidas").html(fallidas);
    $("#lblPending").html(pendientes);
}
