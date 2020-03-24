//TODO
//Ajax webservice usuarios
var id;
var errorFields = [];
var singleOperationRestriction = false;

function addUser(){
    if(!singleOperationRestriction){
        singleOperationRestriction = true;
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
                "active"  : $('#activeInput').prop('checked'),
                "profile" : $('#profileInput').val()
            },
            beforeSend: function(){

            },
            success: function(result){
                if(result.success){
                    FormFunctions.resetFormErrors(errorFields);
                    errorFields = [];
                    $('#successModal').modal('toggle');
                    $('#successModal').modal({backdrop:'static', keyboard:false}); 
                    setTimeout(function(){ 
                        $(location).attr('href', '/users');
                    }, 2000);
                }
                console.log(result);
            },
            error: function (request, status, error, result){
                var details = request.responseJSON.Error.details;
                FormFunctions.resetFormErrors(errorFields);
                errorFields = [];
                FormFunctions.setFormErrors(details);
            },
            complete: function(){
                singleOperationRestriction = false;
            }
        });
    }
}

function updateUser(){
    $.ajax({
        url: '/user/replace',
        method: 'POST',
        async: false,
        dataType: 'json',
        data: {},
        beforeSend: function(){},
        success: function(result){},
        error: function (request, status, error){},
        complete: function(){},
    });
}

function saveFunction(){
    if(id == 0){
        addUser();
    }
    else{
        updateUser();
    }
}

$( document ).ready(function() {
    $('#saveButton').click(function(){
        saveFunction();
    });
});