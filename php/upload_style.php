<?php
header("Content-Type: application/json; charset=utf-8");
include 'db.php';

$target_dir = "print/";
$target_file = $target_dir . $_POST["name"];

if(move_uploaded_file($_FILES["file"]["tmp_name"], $target_file)){
    $image = addslashes(file_get_contents($target_file)); //SQL Injection defence!
    $conn = get_conn();
    $sql = "UPDATE `image` SET `imagen_style` = '$image' WHERE `id` = " . $_POST['id'];
    if ($conn->query($sql) === TRUE) {
        $uploadMessage = "";
        $uploadOk = true;
    } else {
        $uploadMessage = "No se pudo guardar tu imagen";
        $uploadOk = false;
    }
    $conn->close();
}

$response = array(
    'error' => !$uploadOk,
    'message' => $uploadMessage,
    'id' => $_POST['id'],
    'name' => $_POST["name"]
);

echo json_encode($response);
?>
