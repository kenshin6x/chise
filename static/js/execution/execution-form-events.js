if (!$) {
    $ = django.jQuery;
}

$( document ).ready(function() {
    var id_form = "#execution_form";
    var id_site = "#id_site";

    if ($(id_form).length) {
        $(id_site).change(function() {
            $('input[name="_continue"').click();
        });
    }
});