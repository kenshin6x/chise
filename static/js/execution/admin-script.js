// Scripts JQuery para ExecutionModelAdmin
if (!$) {
    $ = django.jQuery;
}

var interval = null;
var last_length = 0;

function runtime_loop(execute_runtime) {
    if (execute_runtime) {
        interval = setInterval(load_checkpoints, 500);
    }
}

function load_checkpoints() {
    $.ajax({
        url: window.location.pathname.replace('execute', 'checkpoints'),
    }).done(function(result){
        var rows = '';
        var row = '';
        var labels = ['Success', 'Fail'];
        var data = {
            'module': {
                'labels': labels,
                'content': [0, 0],
            },
            'script': {
                'labels': labels,
                'content': [0, 0],
            },
        };

        if (result.checkpoints.length > last_length) {
            $(result.checkpoints).each(function(){
                row = $(this)[0];
                rows += '<tr>';
                    rows += '<td>'+ row.reference_display +'</td>';
                    rows += '<td>'+ row.object_display +'</td>';
                    rows += '<td class="'+ (row.status == 1 ? 'td-success' : 'td-fail') +'">'+ row.status_display +'</td>';
                    rows += '<td>'+ row.name +'</td>';
                    rows += '<td>'+ (row.description == null ? '-' : row.description) +'</td>';
                    rows += '<td>'+ row.date_checkpoint +'</td>';
                rows += '</tr>';

                switch(row.object) {
                    case 1:
                        // data['module']['labels'].push(row.name);
                        data['module']['content'][row.status-1]++;
                        break;
                    case 2:
                        // data['script']['labels'].push(row.name);
                        data['script']['content'][row.status-1]++;
                }
            });

            last_length = result.checkpoints.length;
            $('#date-started').html(result.date_started);
        } else {
            return false;
        }

        $('#checkpoints-table tbody').html(rows);

        render_chart(data);

        if (row.reference == 2) {
            clearInterval(interval);
            $('#date-finished').html(result.date_finished);
        }
    });
}

function render_chart(data, type='pie'){
    for(var key in data) {
        var ctx = document.getElementById(key+'-chart');
        var myChart = new Chart(ctx, {
            type: type,
            data: {
                // labels: data[key]['labels'],
                datasets: [{
                    data: data[key]['content'],
                    backgroundColor: [
                        '#12c56e',
                        '#c51212',
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero:true
                        }
                    }]
                },
                // animation: {
                //     duration: 0
                // }
            }
        });
    }
}
