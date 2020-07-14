class StandardCrud{

    constructor(urls){
        this.urls = urls;
    }

    actionPosible(action){
        if (this.urls.hasOwnProperty(action)){
            if(!singleOperationRestriction){
                singleOperationRestriction = true;
                return true;
            }
            console.log(
                "No es posible realizar la acción" + action + "Hay otra operación en curso"
            );
            return false;
        }
        console.log(
            "Error: No hay un metodo para la función " + action
        );
        return false;
    }

    executeAjaxInsideFunction(ajaxFunctions, method, ...args){
        if(ajaxFunctions.hasOwnProperty(method)){
            ajaxFunctions[method](...args);
        }
    }

    makePetition(data, action, ajaxFunctions){
        if(this.actionPosible(action)){
            $.ajax({
                url: this.urls[action].url,
                method: this.urls[action].method,
                async: false,
                dataType: "json",
                data: data,
                beforeSend: () => {
                    this.executeAjaxInsideFunction(ajaxFunctions, 'beforeSend');
                },
                success: (result) => {
                    this.executeAjaxInsideFunction(ajaxFunctions, 'success', result);
                },
                error:  (request, status, error, result) => {
                    this.executeAjaxInsideFunction(ajaxFunctions, 'error', request, status, error, result);
                },
                complete: () => {
                    this.executeAjaxInsideFunction(ajaxFunctions, 'complete');
                    singleOperationRestriction = false;
                }
            });
        }
    }

    standardSuccessModal(result){
        if(result.success){
            FormFunctions.resetFormErrors(errorFields);
            errorFields = [];
            $('#successModal').modal('toggle');
            $('#successModal').modal({backdrop:'static', keyboard:false}); 
            setTimeout(function(){ 
                $(location).attr('href', this.urls['listing_url'].url);
            }, 2000);
        }
    }

    standardError(request){
        var details = request.responseJSON.Error.details;
        FormFunctions.resetFormErrors(errorFields);
        errorFields = [];
        FormFunctions.setFormErrors(details);
    }

    standardSetValue(input, value){
        if(typeof(value) == 'boolean'){
            input.prop("checked", value);
        }
        else{
            input.val(value);
        }
    }

    standardLoadForm(result){
        var data = result.data;
        var keys = Object.keys(data);
        for(field in keys){
            var inputName = "#" + keys[field] + "Input";
            var input = $(inputName);
            setValue(input, data[keys[field]])
        }
    }

    standardDeleteConfirmation(id, deleteModel){
        $('#confirm_button').unbind("click");
        $('#confirm_button').click(function(){
            deleteModel(id);
        });
        $('#idi').html(id);
        $('#cautionModal').modal('toggle');
    }
}