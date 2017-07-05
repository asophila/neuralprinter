<?php

header("Content-Type: text/html; charset=utf-8");
include 'db.php';

$conn = get_conn();


$sql = "SELECT * FROM `code` WHERE `key` = 'test' OR `key` = 'IDangs'";
$result = $conn->query($sql);
echo '<p>Códigos infinitos</><table><tr><th>Código</th><th>Estado</th><th>Imagen<th></tr>';
while ($code = mysqli_fetch_array($result)) {
    echo '<tr><td>'.$code['key'].'</td><td>'.$code['status'].'</td><td>'.$code['image_id'].'</tr>';
}
echo '</table><br>';


$sql = "SELECT * FROM `code` WHERE `key` != 'test' AND `key` != 'IDangs'";
$result = $conn->query($sql);
echo '<p>Códigos desechables</><table><tr><th>ID</th><th>Código</th><th>Estado</th><th>Imagen<th></tr>';
while ($code = mysqli_fetch_array($result)) {
    echo '<tr><td>'.$code['id'].'</td><td>'.$code['key'].'</td><td>'.$code['status'].'</td><td>'.$code['image_id'].'</tr>';
}
echo '</table>';
$conn->close();
?>
