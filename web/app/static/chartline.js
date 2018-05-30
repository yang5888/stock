/**
 * Created by yang on 2018/5/28.
 */
'use strict'

document.write("<script src='https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.js'></script>")

function RandomColor(){
    var color="#";
    for(var i=0;i<6;i++){
        color += (Math.random()*16 | 0).toString(16);
    }
    return color;
}

function lineChart(labels, data, data_label, chart_name, width, height) {
    document.write('<canvas id=\"'+ chart_name + '\" width=\"'+ width + '\" height=\"' + height + '\"></canvas>')
    var lineChartData = {
        type : 'line',
        data : {
            labels : [],
            datasets : []
        }
    }

    for(var i = 0; i< data.length; i++){
        var tmp_data = {}
        tmp_data.data = []
        tmp_data.label = data_label[i]
        for (var j = 0; j< data[i].length; j++){
            tmp_data.data.push(data[i][j])
        }
        tmp_data.backgroundColor = 'transparent'
        tmp_data.borderColor = RandomColor()
        tmp_data.borderWidth = 2
        lineChartData.data.datasets.push(tmp_data)
    }

    for(var i = 0; i <labels.length; i++){
        lineChartData.data.labels.push(labels[i])
    }

    var ctx = document.getElementById(chart_name);
    new Chart(ctx, lineChartData);
}