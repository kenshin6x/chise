// Scripts JQuery para ExecutionModelAdmin
$(document).ready(function(arg) {
    // alert('Rolou');
});

function load_checkpoints(execute_runtime) {
    var runtime_loop = $.ajax({
        url: window.location.pathname.replace('execute', 'checkpoints'),
    }).done(function(result){
        console.log(result);
    });

    if (!execute_runtime) {
        setTimeout(runtime_loop, 500);
    }
}

function show_checkpoints() {

}
