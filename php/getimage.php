<?php

header("Content-Type: text/html; charset=utf-8");
include 'db.php';

$conn = get_conn();
$sql = "SELECT * FROM `image` ORDER BY `id` DESC";
$result = $conn->query($sql);

while ( $row = mysqli_fetch_array($result))
{
    $sql_code = "SELECT * FROM `code` WHERE `image_id` = " . $row['id'];
        $result_code = $conn->query($sql_code);
        if ($result_code->num_rows > 0) {
            $code = $result_code->fetch_assoc();
            $code = $code['key'];
        } else {
            $code = '';
        }
    echo '<p>ID: '.$row['id'].' Nombre: '.$row['name'].$row['ext'].' Estilo: '.$row['estilo'].'</p>';
    echo '<p>Usuario: '.$row['usuario'].' Correo: '.$row['correo'].' Key: '.$code.'</p><br>';
}

$conn->close();
?>
