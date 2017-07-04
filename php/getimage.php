<?php
include 'db.php';

$conn = get_conn();
$sql = "SELECT * FROM image WHERE id = 13";
$sth = $conn->query($sql);
$result=mysqli_fetch_array($sth);
echo '<img src="data:image/jpeg;base64,'.base64_encode( $result['imagen'] ).'"/>';
$conn->close();
?>
