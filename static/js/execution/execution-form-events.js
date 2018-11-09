if (!$) {
    $ = django.jQuery;
}

$( document ).ready(function() {
    var id_form = "#execution_form";

    if ($(execution_form).length) {
        $(id_site).change(function() {
            $('input[name="_continue"').click();
        });
    }
});