<?php
  $path = dirname($_SERVER["SCRIPT_FILENAME"]) . "/data/2021-06-22.json";
  $str = file_get_contents($path);
  $info = json_decode($str, true);

  for ($x = 0; $x <= count($info)-1; $x ++) {
    $final[$x]["x"] = round($info[$x]["time"]);
    $final[$x]["y"] = round($info[$x]["temperatur"]);
  }
  echo json_encode($final, JSON_NUMERIC_CHECK);
  ?>
