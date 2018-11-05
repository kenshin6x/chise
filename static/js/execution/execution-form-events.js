if (!$) {
    $ = django.jQuery;
}

$( document ).ready(function() {
    var id_site = "#id_site";
    var id_modules = "#id_modules";

    if ($(id_site).length) {
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
    }

    $(id_site).change(function() {
        $.getJSON("/core/module/site/" + $(this).val() + "/list/", function( data ) {
            $(id_modules).empty();
            $.each( data, function( key, val ) {
                $(id_modules).append(new Option(val.str, val.pk));
            });
        });
    });
});