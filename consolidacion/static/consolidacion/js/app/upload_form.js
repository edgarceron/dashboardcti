

function getValues(){
    var myFile = $('#inputConsolidacionFile').prop('files')[0];
    let data = new FormData();
    data.append('file', myFile);
    return data;
}

function saveForm(){
    var data = getValues();
    console.log(data);

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
            $('#successModal').modal('toggle');
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

$( document ).ready(function() {
    urls = {
        'upload_consolidacion_url': {'url': upload_consolidacion_url},
    }
    standard = new StandardCrud(urls);

    $('#inputConsolidacionFileAddon').click(function(){
        saveForm();
    });

    $('#inputConsolidacionFile').on('change',function(){

        var fileName = $(this).val();
        $(this).next('.custom-file-label').html(fileName);
    })

});