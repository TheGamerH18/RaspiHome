<?php
  $date = $_GET["date"];
  $path = dirname($_SERVER["SCRIPT_FILENAME"]) . "/data/$date.json";
  $str = file_get_contents($path);
  $info = json_decode($str, true);

  for ($x = 0; $x <= count($info)-1; $x ++) {
    $final[$x]["x"] = round($info[$x]["time"]);
    $final[$x]["y"] = round($info[$x]["temperatur"]);
  }
  echo json_encode($final, JSON_NUMERIC_CHECK);
  ?>
