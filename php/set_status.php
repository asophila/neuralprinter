<?php

function update_status($image_id, $status){
    $conn = get_conn();
    $sql = "UPDATE `image` SET `status` = '$status' WHERE `id` = $image_id";

    $conn->query($sql);

    $conn->close();
    return null;
}

include 'db.php';

update_status($_GET['id'], $_GET['status']);

?>
