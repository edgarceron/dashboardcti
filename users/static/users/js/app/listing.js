$(document).ready(function() {
    $('#listing').dataTable( {
        "processing": true,
        "ajax": {
            "type": "POST",
            "processing": true,
            "url": url,
            "dataSrc": ""
        },

        "columns": [
                { "data": "id" },
                { "data": "username" },
                { "data": "name" },
                { "data": "lastname" }
            ]
    } );
} );