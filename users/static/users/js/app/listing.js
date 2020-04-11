function deleteUser(user_id){
    $.ajax({
        url: user_delete_url + user_id,
        method: 'DELETE',
        async: false,
        dataType: 'json',
        data: {},
        beforeSend: function(){},
        success: function(result){
            $('#modalMessage').html("El usuario ha sido eliminado con exito");
            $('#successModal').modal('toggle');
            $('#successModal').modal({backdrop:'static', keyboard:false}); 
            setTimeout(function(){ 
                location.reload();
            }, 2000);
        },
        error: function (result, request, status, error){},
        complete: function(){
            singleOperationRestriction=false
        },
    });
}

function deleteConfirmation(user_id){
    $('#confirm_button').click(function(){
        deleteUser(user_id);
    });
    $('#idi').html(user_id);
    $('#cautionModal').modal('toggle');
}

$(document).ready(function() {
    var table = $('#listing').dataTable( {
        "processing": true,
        "serverSide": true,
        "ajax": {
            "type": "POST",
            "processing": true,
            "url": url,
            "dataSrc": "data"
        },

        "createdRow": function ( row, data, index ) {
            var jqobj = $(row);
            for(var i = 0;i < 4;i++){
                $('td', row).eq(i).addClass("row_object_id");
                $('td', row).eq(i).attr('user_id', data.id);
            }
            $('td', row).eq(4).attr('user_id', data.id);
            
            if(data.active){
                $('.fa-square', row).addClass('fa-check-square');
                $('.fa-square', row).removeClass('fa-square');
            }
        },

        "columns": [
            { "data": "id" },
            { "data": "username" },
            { "data": "name" },
            { "data": "lastname" },
            { "data": function(){
                var options = '<i class="fas fa-fw fa-trash text-danger"></i>';
                options += '<i class="far fa-fw fa-square text-primary"></i>';
                return options;
            }}
        ], 

        "lengthMenu": [[3, 10, 25, 50], [3, 10, 25, 50]],

        "drawCallback": function( settings ) {
            $('.row_object_id').dblclick(function(event){
                var target = $(event.delegateTarget);
                var id = target.attr('user_id');
                window.location = user_update_url + id;
            });

            $('.fa-trash, .fa-square, .fa-check-square').click(function(event){
                var target = event.target;
                var parent = target.parentElement;
                parent = $(parent);
                target = $(target);
                var user_id = parent.attr('user_id');
                if(target.hasClass('fa-trash')){
                    deleteConfirmation(user_id);
                }
                else if(target.hasClass('fa-square')){
                    console.log('square');
                }
                else if(target.hasClass('fa-check-square')){
                    console.log('check');
                }
            });

            $('.row_object_id').css('cursor', 'pointer'); 
        }
    });

    $('#listing tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
    });


} );