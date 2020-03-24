class FormFunctions{
    static resetFormErrors(errorFields){
        for (const key in errorFields) {
            if (errorFields.hasOwnProperty(key)) {
                const field = errorFields[key];
                const invalid = "#" + field + "Invalid";
                const input   = "#" + field + "Input";
                $(invalid).html("");
                $(input).removeClass("is-invalid");
            }
        }
    }

    static setFormErrors(details){
        for (var key in details) {
            if (details.hasOwnProperty(key)) {
                const field   = details[key].field;
                errorFields.push(field);
                const message = details[key].message;
                const invalid = "#" + field + "Invalid";
                const input   = "#" + field + "Input";
                $(invalid).html(message);
                $(input).addClass("is-invalid");
            }
        }
    }
}