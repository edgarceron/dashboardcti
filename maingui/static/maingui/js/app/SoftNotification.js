class SoftNotification{
    static show(text){
        var topc = 30;
        var className = 'collapse alert alert-info alert-dismissible';

        var iDiv = document.createElement('div');
		iDiv.className = className;
		iDiv.style.position = "fixed";
		iDiv.style.top = '' + topc + 'px';
		iDiv.style.right = "10px";
		iDiv.style.zIndex = "0";
		iDiv.style.width = "50%";
		iDiv.style.cssFloat = "none";
        document.getElementsByTagName('body')[0].appendChild(iDiv);
        
        var closeButton = '<button type="button" class="close" data-dismiss="alert"'
        + 'aria-label="Close"><span aria-hidden="true">&times;'
        + '</span></button>'
        $(iDiv).html(text + closeButton);
        $(iDiv).collapse('show');

        setTimeout(function(){
            $(iDiv).collapse('hide');
        }, 5000);
    }
}