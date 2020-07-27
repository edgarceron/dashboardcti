

function getValues(){
    var myFile = $('#inputConsolidacionFile').prop('files')[0];
    let data = new FormData();
    data.append('file', myFile);
    return data;
}

function saveForm(){
    var data = getValues();
    $.ajax({
        url: upload_consolidacion_url,
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
            standard.standardError(request, status, error, result);
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
    urls = {
        'upload_consolidacion_url': {'url': upload_consolidacion_url},
    }
    standard = new StandardCrud(urls);

    $('#inputConsolidacionFileAddon').click(function(){
        saveForm();
    });

    $('#inputConsolidacionFile').on('change',function(){
        var fileName = splitFileName($(this).val());
        $(this).next('.custom-file-label').html(fileName);
    })

});