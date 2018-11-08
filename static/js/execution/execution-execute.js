// Scripts JQuery para ExecutionModelAdmin
if (!$) {
    $ = django.jQuery;
}

$(document).ready(function(){
    $('#content-main').fadeIn('slow');
    $('#open-dialog-chart-button').click();
});

$('#open-dialog-chart-button').click(function() {
    $('#chart-modal').dialog({
        title: "Charts",
        minWidth: 500,
        minHeight: 300,
        position: { my: "center", at: 'right' }
    });
});

var interval = null;
var last_length = 0;
var first_execution = true;

function runtime_loop(execute_runtime) {
    if (execute_runtime) {
        interval = setInterval(load_checkpoints, 500);
    } else {
        load_checkpoints();
    }
}

function load_checkpoints() {
    $.ajax({
        url: window.location.pathname.replace('execute', 'checkpoints'),
    }).done(function(result){
        var rows = '';
        var row = '';
        var data = {
            'progress': {
                'labels': ['Execution Progress'],
                'content': [],
                'type-chart': 'horizontalBar',
                'extra-options': {
                    scales: {
                        xAxes: [{
                            ticks: {
                                min: 0,
                                max: 100,
                                callback: function(value, index, values) {
                                    return value + '%';
                                },
                            },
                        }],
                    },
                }
            },
            'module': {
                'labels': ['Success', 'Fail'],
                'content': [],
                'type-chart': 'doughnut',
                'extra-options': {},
            }
        };

        if (result.checkpoints.length <= last_length && result.status.toLowerCase() != 'finished') {
            return false;
        } else if (result.status.toLowerCase() == 'finished') {
            clearInterval(interval);
        }

        $(result.checkpoints).each(function(){
            row = $(this)[0];
            
            rows += '<tr class="'+ (row.status == 1 ? 'tr-success' : 'tr-fail') +'">';
                rows += '<td>'+ row.reference_display +'</td>';
                rows += '<td>'+ row.object_display +'</td>';
                rows += '<td>'+ row.status_display +'</td>';
                rows += '<td>'+ row.name +'</td>';
                rows += '<td>'+ (row.description == null ? '-' : row.description) +'</td>';
                rows += '<td>'+ row.date_checkpoint +'</td>';
            rows += '</tr>';            
        });

        last_length = result.checkpoints.length;
        $('#date-started').html(result.date_started);
        $('#execution-status').html(result.status).attr('class', result.status.toLowerCase());
        $('#checkpoints-table tbody').html(rows);

        if (row.object == 1 && row.reference == 2 || first_execution) {
            data['progress']['content'][0] = [(result.report.modules_finished_count/result.report.modules_count)*100];
            data['module']['content'] = [result.report.modules_finished_success_count, result.report.modules_finished_fail_count];
            render_chart(data);
            first_execution = false;
        }

        if (row.reference == 2 && result.date_finished != null) {
            $('#content-main .object-tools a').fadeIn('slow');
            $('#date-finished').html(result.date_finished);
        }
    });
}

function render_chart(data){
    for(var key in data) {
        var baseOptions = {
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: key.toUpperCase(),
                position: 'top'
            },
            responsive: true,
            layout: {
                padding: {
                    left: 10,
                    right: 10,
                    top: 10,
                    bottom: 15
                }
            }
        }

        var ctx = document.getElementById(key+'-chart');
        var myChart = new Chart(ctx, {
            type: data[key]['type-chart'],
            data: {
                labels: data[key]['labels'],
                datasets: [{
                    data: data[key]['content'],
                    backgroundColor: [
                        '#69F0AE',
                        '#ffcdd2'
                    ],
                    borderWidth: 3
                }]
            },
            options: extend(baseOptions, data[key]['extra-options'])
        });
    }
}

function extend(obj, src) {
    for (var key in src) {
        if (src.hasOwnProperty(key)) obj[key] = src[key];
    }

    return obj;
}
