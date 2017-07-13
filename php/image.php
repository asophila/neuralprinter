<?php
include 'db.php';

if(isset($_GET['id'])){

    $conn = get_conn();
    $sql = "SELECT * FROM `image` WHERE `id` = " . $_GET['id'];
    $result = $conn->query($sql);

    $row = mysqli_fetch_array($result);

    if($row['imagen']){
        echo '<img src="data:image/jpeg;base64,'.base64_encode( $row['imagen'] ).'"/>';
    } else {
        echo '<p>Sin imagen</p>';
    }
}
?>
