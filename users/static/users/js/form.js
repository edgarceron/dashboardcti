//TODO
//Ajax webservice usuarios

function addUser(){
    $.ajax({
        url: "/users/add",
        method: "POST",
        async: false,
        dataType: "json",
        data: {
            "name"    : $('#nameInput').val(),
            "lastname": $('#lastnameInput').val(),
            "username": $('#usernameInput').val(),
            "password": $('#passwordInput').val(),
            "active"  : $('#activeInput').val(),
            "profile" : $('#profileInput').val()
        },
        beforeSend: function(){

        },
        success: function(result){
            console.log(result);
        },
        error: function (request, status, error){
            console.log('Hubo un error');
        },
        complete: function(){

        }
    })
}