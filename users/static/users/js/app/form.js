//TODO
//Ajax webservice usuarios
var id;
var listing_url;
var errorFields = [];
var singleOperationRestriction = false;

function addData(){
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
                        $(location).attr('href', listing_url);
                    }, 2000);
                }
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

function updateData(user_id){
    $.ajax({
        url: replace_url + user_id,
        method: 'PUT',
        async: false,
        dataType: 'json',
        data: {
            "name"    : $('#nameInput').val(),
            "lastname": $('#lastnameInput').val(),
            "username": $('#usernameInput').val(),
            "password": $('#passwordInput').val(),
            "active"  : $('#activeInput').prop('checked'),
            "profile" : $('#profileInput').val()
        },
        beforeSend: function(){},
        success: function(result){
            if(result.success){
                FormFunctions.resetFormErrors(errorFields);
                errorFields = [];
                $('#successModal').modal('toggle');
                $('#successModal').modal({backdrop:'static', keyboard:false}); 
                setTimeout(function(){ 
                    $(location).attr('href', listing_url);
                }, 2000);
            }
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

function getData(user_id){
    $.ajax({
        url: '/users/get/' + user_id,
        method: 'POST',
        async: false,
        dataType: 'json',
        data: {},
        beforeSend: function(){},
        success: function(result){
            var data = result.data;
            var keys = Object.keys(data);
            for(field in keys){
                var inputName = "#" + keys[field] + "Input";
                var input = $(inputName);
                setValue(input, data[keys[field]])
            }
        },
        error: function (request, status, error){},
        complete: function(){},
    });
}

function setValue(input, value){
    if(typeof(value) == 'boolean'){
        input.prop("checked", value);
    }
    else{
        input.val(value);
    }
}


function saveFunction(){
    if(id == 0){
        addData();
    }
    else{
        updateData(id);
    }
}

$( document ).ready(function() {
    $('#saveButton').click(function(){
        saveFunction();
    });
});