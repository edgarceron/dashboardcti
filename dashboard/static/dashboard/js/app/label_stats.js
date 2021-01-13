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

function setStatsOperationsEntry(citas_count, polls_attended){
    $("#lblCitasAgendadas").html(citas_count);
    $("#lblEncuestasRealizadas").html(polls_attended);
}

function setStatsOperations(consolidacion_count, polls_attended){
    $("#lblConsolidacion").html(consolidacion_count);
    $("#lblPollsMade").html(polls_attended);
}

function setStatsAverage(average){
    time = new Date(average * 1000).toISOString().substr(11, 8);
    $("#lblAverageTimeOut").html(time);
}

function setStatsAverageEntry(average){
    time = new Date(average * 1000).toISOString().substr(11, 8);
    $("#lblAverageTime").html(time);
}

function setScheduledLabel(scheduled){
    $("#lblScheduled").html(scheduled);
}

function setStatsLabelsOut(callsCount){
    var pendientes = callsCount["Placing"] + callsCount[null];
    var fallidas = callsCount["Abandoned"] + callsCount["Failure"] + callsCount["ShortCall"] + callsCount["NoAsnwer"];
    $("#lblTotalOut").html(callsCount["total"]);
    $("#lblTerminadasOut").html(callsCount["Success"]);
    $("#lblFallidas").html(fallidas);
    $("#lblPending").html(pendientes);

}
