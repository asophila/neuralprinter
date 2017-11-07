<?php
include 'db.php';

if(isset($_GET['id'])){

    $conn = get_conn();
    $sql = "SELECT * FROM `image` WHERE `id` = " . $_GET['id'];
    $result = $conn->query($sql);

    $row = mysqli_fetch_array($result);


    echo '<p>Nombre: <b>'.$row['usuario'].'</b></p>';
    echo '<p>Correo: <b>'.$row['correo'].'</b></p>';

    if($row['imagen']){
        echo '<img width="400" src="data:image/jpeg;base64,'.base64_encode( $row['imagen'] ).'"/>';
    } else {
        echo '';
    }

    if($row['imagen_style']){
        echo '<img width="400" src="data:image/jpeg;base64,'.base64_encode( $row['imagen_style'] ).'"/>';
    } else {
        echo '';
    }
}
?>
