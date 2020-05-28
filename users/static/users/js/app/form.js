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
            url: add_url,
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
        url: get_url + user_id,
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
                if(inputName == "#profileInput"){
                    getProfileData(data[keys[field]]);
                }
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

function updatePicker(pickerName, value, text){
    var input = $(pickerName);
    input.html('');
    var option = `<option value="${value}">${text}</option>`;
    input.append(option);
    input.selectpicker("refresh");
}

function getProfileData(id_profile){ 
    if(id_profile != null){
        $.ajax({
            url: get_profile_url + id_profile,
            method: 'POST',
            async: false,
            dataType: 'json',
            success: function(result){
                if(result.success){
                    profile = result.data;
                    if(profile != null){
                        var opVal = profile.id;
                        var opText = profile.name;
                        pickerName = '#profileInput';
                        updatePicker(pickerName, opVal, opText);
                    }
                }
            }
        });
    }
}

$( document ).ready(function() {
    
    $('#saveButton').click(function(){
        saveFunction();
    });

    $('#profileInput').selectpicker(
        {
            "liveSearch": true
        }
    );

    if(id != 0){
        getData(id);
    }

    $('#profileInput').siblings().find("input[type='text']").keyup(
        function(event){
            var target = $(event.target);
            var text = target.val();
            if(text.length > 1){
                $.ajax({
                    url: list_profile_url,
                    method: 'POST',
                    async: false,
                    dataType: 'json',
                    data: {'value': text},
                    beforeSend: function(){},
                    success: function(result){
                        if(result.success){
                            data = result.result[0];
                            pickerName = '#profileInput';
                            var opVal = data.id;
                            var opText = data.name;
                            updatePicker(pickerName, opVal, opText);
                        }
                    },
                    error: function (result, request, status, error){},
                    complete: function(){
                        singleOperationRestriction=false
                    },
                });
            }
        }
    )
});