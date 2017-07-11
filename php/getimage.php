<!DOCTYPE html>
<html lang="es">
<head>
    <base href="./">
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Practia te pinta | Practia</title>
    <meta name="description" content="">
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="icon" href="images/favicon.ico" type="image/x-icon">
    <!-- inject:css -->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.min.css" media="screen,projection" />
    <link href="css/less-space.css" rel="stylesheet" type="text/css">
    <link type="text/css" rel="stylesheet" href="css/practia.css" media="screen,projection" />
    <!-- endinject -->
</head>

<body>
    <!-- Start Page Loading -->
    <div id="loader-wrapper">
        <div id="loader"></div>        
        <div class="loader-section section-left"></div>
        <div class="loader-section section-right"></div>
    </div>
    <!-- End Page Loading -->
    <header>
        <div class="navbar-fixed">
        <nav>
            <div class="nav-wrapper z-depth-1"> <a href="./" class="brand-logo"><img src="images/logo.png" alt="Practia" class="responsive-img" ></a> </div>
        </nav>
        </div>
    </header>
    <main class="xs-pl-20 xs-pr-20">
        <div class="row center-align"> <button id="btnExport" class="btn waves-effect waves-light btn-large" type="submit" name="action"><i class="material-icons right">file_download</i>Descargar Excel</button></div>
        <div id="data" class="row center-align">
            <table class="striped">
                <thead>
            <tr><th></th><th>Nombre</th><th>Correo</th><th>Empresa</th><th>Cargo</th><th>Código</th><th>Evento</th><th>Estilo</th><th>Imagen</th><th>Estado</th><th>Fecha</th></tr>
</thead><tbody>
<?php
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
    echo '<tr>';
    echo '<td>'.$row['id'].'</td><td>'.$row['usuario'].'</td><td>'.$row['correo'].'</td>';
    echo '<td>'.$row['empresa'].'</td><td>'.$row['cargo'].'</td><td>'.$code.'</td><td>'.$row['ip'].'</td>';
    echo '<td>'.$row['estilo'].'</td><td>'.$row['name'].$row['ext'].'</td><td>'.$row['status'].'</td><td>'.$row['timestamp'].'</td>';
    echo '</tr>';
}

$conn->close();
?>
</tbody>
        </table>
        </div>
    </main>
    <footer> </footer>
<!-- inject:css -->
    <script type="text/javascript" src="js/jquery.min.js"></script>
    <script type="text/javascript" src="js/materialize.min.js"></script>
    <script type="text/javascript" src="js/practia.js"></script>
    <script>
        $("#btnExport").click(function (e) {
            e.preventDefault();

            //getting data from our table
            var data_type = 'data:application/vnd.ms-excel';
            var table_div = document.getElementById('data');
            var table_html = table_div.outerHTML.replace(/ /g, '%20');

            var a = document.createElement('a');
            a.href = data_type + ', ' + table_html;
            a.download = 'practiapintame_' + Math.floor((Math.random() * 9999999) + 1000000) + '.xls';
            a.click();
        });

        $(document).ready(function(){
            setTimeout(function() {
                $("body").addClass("loaded");
            }, 200);
        });
    </script>
</body>

</html>
