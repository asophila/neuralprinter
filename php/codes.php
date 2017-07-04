<?php

function valid_code($code){
    $conn = get_conn();
    $sql = "SELECT * FROM `code` WHERE `key` = '$code'";

    $result = $conn->query($sql);
    $response = array();
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        if($row['status'] < 1){
            $response = array(
                'valid' => true,
                'message' => '',
                'code' => $code
            );
        } else {
            $response = array(
                'valid' => false,
                'message' => 'El código ya ha sido usado',
                'code' => $code
            );
        }
    } else {
        $response = array(
            'valid' => false,
            'message' => 'El código no es válido',
            'code' => $code
        );
    }
    $conn->close();
    return json_encode($response);
}

function get_next_to_process(){
    $conn = get_conn();
    $sql = "SELECT * FROM `image` WHERE `status` = 'A_PROCESAR' ORDER BY `id` ASC";

    $result = $conn->query($sql);
    $response = array();
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();

        $response = array(
            'error' => false,
            'message' => '',
            'name' => $row['name'],
            'ext' => $row['ext'],
            'estilo' => $row['estilo'],
            'imagen' => base64_encode( $row['imagen'] )
        );
    } else {
        $response = array(
            'error' => true,
            'message' => 'No hay más por procesar'
        );
    }
    $conn->close();
    return json_encode($response);
}

#header("Content-Type: application/json; charset=utf-8");
#include 'db.php';

if (isset($_GET['func']) && $_GET['func'] == 'get_next_to_process'){
    include 'db.php';
    echo get_next_to_process();
}

?>
