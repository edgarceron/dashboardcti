class StandardCrud{

    constructor(urls){
        this.urls = urls;
        this.async = false;
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
                async: this.async,
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

    standardGetError(result){
        if (result.error){
            SoftNotification.show(result.error, "danger");
        }
        else {
            SoftNotification.show("Ha ocurrido un error de servidor o conexión", "danger");
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

    static standardDeleteConfirmation(id, deleteModel){
        $('#confirm_button').unbind("click");
        $('#confirm_button').click(function(){
            deleteModel(id);
        });
        $('#idi').html(id);
        $('#cautionModal').modal('toggle');
    }

    standardListingButtonsFunction(event, deleteModel, toogleModel){
        var target = event.target;
        var parent = target.parentElement;
        parent = $(parent);
        target = $(target);
        var model_id = parent.attr('model_id');
        if(target.hasClass('fa-trash')){
            StandardCrud.standardDeleteConfirmation(model_id, deleteModel);
        }
        else if(target.hasClass('fa-square') || target.hasClass('fa-check-square')){
            toogleModel(model_id, target);
        }
    }
    
    standardCreatedRow(row, data, index){
        var count = row.cells.length 
        var data_rows = count - 2;
        var options_row = count -1;
        for(var i = 0;i < data_rows;i++){
            $('td', row).eq(i).addClass("row_object_id");
            $('td', row).eq(i).attr('model_id', data.id);
        }
        $('td', row).eq(options_row).attr('model_id', data.id);
        
        if(data.active){
            $('.fa-square', row).addClass('fa-check-square');
            $('.fa-square', row).removeClass('fa-square');
        }
    }

    standardDatatable(columns, deleteModel, toogleModel){
        var standardCreatedRow = this.standardCreatedRow;
        var standardListingButtonsFunction = this.standardListingButtonsFunction;
        if(deleteModel != null || toogleModel != null){
            columns.push({ "data": function(){
                var options = "";
                if(deleteModel != null)
                    options += '<i class="fas fa-fw fa-trash text-danger"></i>';            
                if(toogleModel != null)
                    options += '<i class="far fa-fw fa-square text-primary"></i>';
                return options;
            }});
        }

        var table = $('#listing').dataTable( {
            "processing": true,
            "serverSide": true,
            "ajax": {
                "type": "POST",
                "processing": true,
                "url": this.urls['data_list_url'].url,
                "dataSrc": "data"
            },
    
            "createdRow": function ( row, data, index ) {
               standardCreatedRow(row, data, index)
            },
    
            "columns": columns, 
    
            "lengthMenu": [[10, 25, 50], [10, 25, 50]],
    
            "drawCallback": function( settings ) {
                $('.row_object_id').dblclick(function(event){
                    var target = $(event.delegateTarget);
                    var id = target.attr('model_id');
                    window.location = update_url + id;
                });
    
                $('.fa-trash, .fa-square, .fa-check-square').click(function(event){
                    standardListingButtonsFunction(event, deleteModel, toogleModel);
                });
    
                $('.row_object_id').css('cursor', 'pointer'); 
    
                $(function () {
                    $('[data-toggle="popover"]').popover()
                });
            }
        });
    
        $('#listing tbody').on( 'click', 'tr', function () {
            $(this).toggleClass('selected');
        });
    }

    standardToggleSuccess(result, square_element, model_name){
        if(result.success){
            if(square_element.hasClass('fa-square')){
                square_element.removeClass('fa-square');
                square_element.addClass('fa-check-square');
                SoftNotification.show(model_name + " activado con exito");
            }
            else if(square_element.hasClass('fa-check-square')){
                square_element.removeClass('fa-check-square');
                square_element.addClass('fa-square');
                SoftNotification.show(model_name + " desactivado con exito");
            }
        }
    }

    standardDeleteSuccess(model_name){
        $('#modalMessage').html(model_name + " eliminado/a con exito");
        $('#successModal').modal('toggle');
        $('#successModal').modal({backdrop:'static', keyboard:false}); 
        setTimeout(function(){ 
            location.reload();
        }, 2000);
    }

    standardSetValues(result){
        var data = result.data;
        var keys = Object.keys(data);
        for(var field in keys){
            var inputName = "#" + keys[field] + "Input";
            var input = $(inputName);
            this.loadPicker(keys[field], data[keys[field]]);
            FormFunctions.setValue(input, data[keys[field]]);
        }
    }

    loadPicker(field, model_id){
        var url = "get_" + field  + "_url";
        if(url in this.urls && model_id != null){
            $.ajax({
                url: this.urls[url].url + model_id,
                method: 'POST',
                async: this.async,
                dataType: 'json',
                success: function(result){
                    if(result.success){
                        var data = [result.data];
                        if(data != null){
                            var pickerName = '#' + field + 'Input';
                            FormFunctions.updatePicker(pickerName, data);
                        }
                    }
                }
            });
        }
    }
}