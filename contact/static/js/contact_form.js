jQuery(function() {
    var form = jQuery("#ContactForm");
    form.submit(function(e) {
        jQuery("#id_sendbutton").attr('disabled', true)
        jQuery("#sendwrapper").prepend('<span>Sending message, please wait... </span>')
        jQuery("#ajaxwrapper").load(
            form.attr('action') + ' #ajaxwrapper',
            form.serializeArray(),
            function(responseText, responseStatus) {
                jQuery("#id_sendbutton").attr('disabled', false)
                if (responseText == 'redirect'){
                    window.location = '/'
                }
            }
        );
        e.preventDefault();
    });
});
