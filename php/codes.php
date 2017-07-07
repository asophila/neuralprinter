<?php

function valid_code($code){
    if(empty($code)){
        $response = array(
                    'valid' => true,
                    'message' => '',
                    'code' => ''
                );
    } else {
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
    }
    return json_encode($response);
}

?>
