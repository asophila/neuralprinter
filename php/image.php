<?php
include 'db.php';

$conn = get_conn();
$sql = "SELECT * FROM image WHERE id = " . $_GET['id'];
$sth = $conn->query($sql);
$result=mysqli_fetch_array($sth);
echo '<img width="600" src="data:image/jpeg;base64,'.base64_encode( $result['imagen'] ).'"/>';
$conn->close();
?>
