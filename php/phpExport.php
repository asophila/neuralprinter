<?php

$servername = "localhost";
$username = "";
$password = "";
$dbname = "";
$file = "file.sql";

$no_create_info = true;
$no_create = ' --no-create-info';
if(!$no_create_info){
    $no_create = '';
}

$ignore_code = true;
$ignore = ' --ignore-table='.$dbname.'.code';
if(!$ignore_code){
    $ignore = '';
}

$command = 'mysqldump --user='.$username.' --password='.$password.' --host='.$servername.' '.$dbname;
$command = $command.$no_create.$ignore.' | gzip > '.$file.'.gz';

exec($command);
?>
