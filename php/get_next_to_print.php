<?php

function get_next_to_print(){
    $conn = get_conn();
    $sql = "SELECT * FROM `image` WHERE `status` = 'PROCESADO' ORDER BY `id` ASC";

    $result = $conn->query($sql);
    $response = array();
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();

        $sql_code = "SELECT * FROM `code` WHERE `image_id` = " . $row['id'];
        $result_code = $conn->query($sql_code);
        if ($result_code->num_rows > 0) {
            $code = $result_code->fetch_assoc();
            $code = $code['key'];
        } else {
            $code = '';
        }

        $response = array(
            'error' => false,
            'message' => '',
            'id' => $row['id'],
            'codigo' => $code,
            'correo' => $row['correo'],
            'name' => $row['name'] . '_'. $row['estilo'],
            'ext' => $row['ext'],
            'imagen' => base64_encode( $row['imagen_style'] )
        );
    } else {
        $response = array(
            'error' => true,
            'message' => 'No hay más por imprimir'
        );
    }
    $conn->close();
    return json_encode($response);
}

header("Content-Type: application/json; charset=utf-8");
include 'db.php';

echo get_next_to_print();

?>
