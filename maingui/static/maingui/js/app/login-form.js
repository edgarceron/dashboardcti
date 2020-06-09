function getValues(){
    var data = {
        "username"    : $('#inputEmail').val(),
        "password"    : $('#inputPassword').val(),
        "rememberMe"  : $('#inputRemember').prop('checked')
    }
    return data;
}

function login(){
    if(!singleOperationRestriction){
        singleOperationRestriction = true;
        $.ajax({
            url: login_url,
            method: 'POST',
            async: false,
            dataType: 'json',
            data: getValues(),
            beforeSend: function(){},
            success: function(result){
                if(result.success){
                    $(location).attr('href', index_url);
                }
                else{
                    SoftNotification.show("Error: " + result.message, "danger");
                }
            },
            error: function (result, request, status, error){
                SoftNotification.show("Error: No hay conexión o hubo un fallo en el servidor");
            },
            complete: function(){
                singleOperationRestriction=false
            },
        });
    }
}