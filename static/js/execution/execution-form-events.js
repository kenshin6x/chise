if (!$) {
    $ = django.jQuery;
}

$( document ).ready(function() {
    var execution_form = "#execution_form";
    var id_site = "#id_site";
    var id_modules = "#id_modules";
    var add_id_modules = "#add_id_modules";
    var add_id_modules_href = $(add_id_modules).attr('href');

    if ($(execution_form).length) {
        if ($(id_site).val()) {
            $(add_id_modules).attr('href', add_id_modules_href + '&site_id=' + $(id_site).val());
        }
        
        $.getJSON("/core/module/site/" + $(id_site).val() + "/list/", function( data ) {
            var items = []

            $.each( data, function( key, val ) {
                items.push(val.pk)
            });

            $(id_modules + " option").each(function() {
                if(!items.includes(parseInt($(this).val()))) {
                    $(this).remove();
                }
            });
        });

        $(id_site).change(function() {
            $(add_id_modules).attr('href', add_id_modules_href + '&site_id=' + $(id_site).val());

            $.getJSON("/core/module/site/" + $(this).val() + "/list/", function( data ) {
                $(id_modules).empty();
                $.each( data, function( key, val ) {
                    $(id_modules).append(new Option(val.str, val.pk));
                });
            });
        });
    }
});