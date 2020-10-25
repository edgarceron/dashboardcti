

function getValues(){
    var myFile = $('#inputFile').prop('files')[0];
    let data = new FormData();
    data.append('file', myFile);
    data.append('id', id);
    return data;
}

function saveForm(){
    var data = getValues();
    $.ajax({
        url: upload_url,
        method: 'POST',
        async: true,
        cache: false,
        processData: false,
        contentType: false,
        dataType: "json",
        data: data,
        beforeSend: () => {
            $('#spiner').removeClass('d-none');
        },
        success: (result) => {
            if(result.fails.length > 0){
                SoftNotification.show("Subido con exito, abajo aparecen los errores");
                var text = "";
                for(var i = 0; i<result.fails.length;i++){
                    text += result.fails[i] + "\n";
                }
                $('#failsArea').val( text );
                $('#divArea').removeClass('d-none');
            }
            else{
                SoftNotification.show("Subido con exito");
            }
        },
        error:  (request, status, error, result) => {
            SoftNotification.show("Hubo un error al intentar subir el archivo", "danger")
        },
        complete: () => {
            $('#spiner').addClass('d-none');
            singleOperationRestriction=false
        }
    });
}

function splitFileName(str) {
    return str.split('\\').pop().split('/').pop();
}

$( document ).ready(function() {

    $('#saveButton').click(function(){
        saveForm();
    });

    $('#inputFile').on('change',function(){
        var fileName = splitFileName($(this).val());
        $(this).next('.custom-file-label').html(fileName);
    })

});