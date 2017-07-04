<?php
header("Content-Type: application/json; charset=utf-8");
include 'db.php';

$target_dir = "print/";
$target_file = $target_dir . $_POST["name"];
$file_content = base64_decode($_POST["imagen"]);

if(file_put_contents($target_file, $file_content)){
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
    'error' => $uploadOk,
    'message' => $uploadMessage,
    'id' => $_POST['id'],
    'name' => $_POST["name"]
);

echo json_encode($response);
?>
