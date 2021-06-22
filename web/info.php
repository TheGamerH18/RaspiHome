<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <link rel="stylesheet" href="style.css">
    <meta http-equiv="refresh" content="10">
    <meta charset="utf-8">
    <script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script>

      window.onload = function() {
        var datapoints1;
        $.get("/home/temperatur.php", {date=""}, function(data) {
          datapoints1 = JSON.parse(data);
        });
        var interval = 5000

        var chart = new CanvasJS.Chart("chartContainer", {
          zoomEnabled: true,
          theme: "dark1",
          title: {
            text: "Temperatur"
          },
          axisY: {
            suffix: " °C"
          },
          toolTip: {
            shared: true
          },
          data: [{
            type: "line",
            name: "Temperatur",
            xValueType: "dateTime",
            yValueFormatString: "# °C",
            xValueFormatString: "hh:mm:ss",
            dataPoints: datapoints1
          }]
        });

				chart.render();

        function toggleDataSeries(e) {
          if(typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
            e.dataSeries.visible = false;
          } else {
            e.dataSeries.visible = true;
          }
          chart.render();
        }

      }
    </script>
    <title></title>
  </head>
  <body>
    <div id="chartContainer">

    </div>
  </body>
</html>
