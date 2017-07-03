<?php

function get_conn() {
    $servername = "localhost";
    $username = "crappyla_tepinta";
    $password = "Espej0Espej0";
    $dbname = "crappyla_tepinta";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
        return null;
    }
    return $conn;
}


#$conn = get_conn();
#$conn->close();

?>
