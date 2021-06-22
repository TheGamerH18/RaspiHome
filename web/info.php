<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <link rel="stylesheet" href="style.css">
    <meta charset="utf-8">
    <script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script>

      window.onload = function() {
        var datapoints1 = [];
        var interval = 30000;

        var chart = new CanvasJS.Chart("chartContainer", {
          zoomEnabled: true,
          theme: "dark1",
          title: {
            text: "Temperatur"
          },
          axisY: {
            suffix: " Â°C"
          },
          toolTip: {
            shared: true
          },
          data: [{
            type: "line",
            name: "Temperatur",
            xValueType: "dateTime",
            yValueFormatString: "# Â°C",
            xValueFormatString: "hh:mm:ss",
            dataPoints: datapoints1
          }]
        });

        function toggleDataSeries(e) {
          if(typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
            e.dataSeries.visible = false;
          } else {
            e.dataSeries.visible = true;
          }
          chart.render();
        }

        function updateChart() {
          $.getJSON("/home/temperatur.php", {date: ""}, function(data) {
            chartupdate(data);
          });
        }

        function chartupdate(data) {
          datapoints1.splice(0, datapoints1.length);
          $.each(data, function(key, value){
            datapoints1.push({x: value["x"], y: value["y"]})
          });
          console.log(datapoints1);
          chart.render();
        }

        setInterval(function(){updateChart()}, interval);

      }
    </script>
    <title></title>
  </head>
  <body>
    <div id="chartContainer">

    </div>
  </body>
</html>
