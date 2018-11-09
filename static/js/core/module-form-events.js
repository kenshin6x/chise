if (!$) {
    $ = django.jQuery;
}

$( document ).ready(function() {
    var id_form = "#module_form";
    var id_group = "#id_group";

    if ($(id_form).length) {
        $(id_group).change(function() {
            $('input[name="_continue"').click();
        });
    }
});