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
        var datapoints1 = <?php
          $path = dirname($_SERVER["SCRIPT_FILENAME"]) . "/data/2021-06-22.json";
          $str = file_get_contents($path);
          $info = json_decode($str, true);

          for ($x = 0; $x <= count($info)-1; $x ++) {
            $final[$x]["x"] = round($info[$x]["time"]);
            $final[$x]["y"] = round($info[$x]["temperatur"]);
          }
          echo json_encode($final, JSON_NUMERIC_CHECK);
          ?>;
        var interval = 5000

        var chart = new CanvasJS.Chart("chartContainer", {
          zoomEnabled: true,
          theme: "dark1",
          title: {
            text: "Temperatur"
          },
          axisX: {
            title: "Chart updates every some seconds"
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
  <body><?php
      echo $final[count($final) - 1]["y"]
      ?> °C
    <div id="chartContainer">

    </div>
  </body>
</html>
