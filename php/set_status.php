<?php

function update_status($image_id, $status){
    $conn = get_conn();
    $sql = "UPDATE `image` SET `status` = '$status' WHERE `id` = $image_id";

    $conn->query($sql);

    $conn->close();
    return true;
}

include 'db.php';

$result = update_status($_POST['id'], $_POST['status']);
$response = array(
            'error' => !$result,
            'message' => ''
        );
echo json_encode($response);
?>
