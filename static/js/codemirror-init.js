if (!$) {
    $ = django.jQuery;
}

$( document ).ready(function() {
    window.editor = CodeMirror.fromTextArea(document.getElementById('id_code'), {
        mode: "python",
        indentWithTabs: true,
        smartIndent: true,
        lineNumbers: true,
        matchBrackets : true,
        autofocus: true,
        theme: "monokai",
        extraKeys: {
            "Ctrl-Space": "autocomplete"
        }
    });
});