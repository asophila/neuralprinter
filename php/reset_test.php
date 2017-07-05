<?php
include 'db.php';

$conn = get_conn();
$sql = "UPDATE `code` SET `status` = 0, `image_id`= NULL WHERE `key`= 'test'";
$conn->query($sql);
echo '<p></p>';
$conn->close();
?>
