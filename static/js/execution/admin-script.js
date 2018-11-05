// Scripts JQuery para ExecutionModelAdmin
if (!$) {
    $ = django.jQuery;
}

var interval = null;

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
        var labels = [];
        var data = [];

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

            labels.push(row.name);
            data.push(row.reference);
        });

        $('#checkpoints-table tbody').html(rows);
        render_chart(labels, data);

        if (row.reference == 2) {
            clearInterval(interval);
            window.location.reload();
        }
    });
}

function render_chart(labels, data, type='line'){
    var ctx = document.getElementById("myChart");
    var myChart = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: '# of Votes',
                data: data,
                // backgroundColor: [
                //     'rgba(255, 99, 132, 0.2)',
                //     'rgba(54, 162, 235, 0.2)',
                //     'rgba(255, 206, 86, 0.2)',
                //     'rgba(75, 192, 192, 0.2)',
                //     'rgba(153, 102, 255, 0.2)',
                //     'rgba(255, 159, 64, 0.2)'
                // ],
                // borderColor: [
                //     'rgba(255,99,132,1)',
                //     'rgba(54, 162, 235, 1)',
                //     'rgba(255, 206, 86, 1)',
                //     'rgba(75, 192, 192, 1)',
                //     'rgba(153, 102, 255, 1)',
                //     'rgba(255, 159, 64, 1)'
                // ],
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
            animation: {
                duration: 0
            }
        }
    });
}
