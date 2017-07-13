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
        
        <div class="row">
            <div class="input-field col s12">
                <i class="material-icons prefix">search</i>
                <input name="filtro" id="filtro" type="text" placeholder="Filtrar por Nombre, Correo o Estado" onkeyup="filtrar()">
                <label for="filtro">Filtrar</label>
            </div>
        </div>
        <div id="data" class="row center-align">
            <table class="striped">
                <thead>
            <tr><th></th><th>Nombre</th><th>Correo</th><th>Empresa</th><th>Cargo</th><th>Código</th><th>Evento</th><th>Estilo</th><th>Imagen</th><th>Estado</th><th>Fecha</th></tr>
</thead><tbody>
<?php
include 'db.php';


$limit = 50;
if(isset($_GET['limit'])){
    $limit = $_GET['limit'];
}

$conn = get_conn();
$sql = "SELECT * FROM `image` ORDER BY `id` DESC LIMIT " . $limit;
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
    echo '<td>'.$row['estilo'].'</td><td><a target="_blank" href="./image.php?id='.$row['id'].'">'.$row['name'].$row['ext'].'</a></td><td>'.$row['status'].'</td><td>'.$row['timestamp'].'</td>';
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
    <script>
        function filtrar() {
        // Declare variables 
        var input, filter, table, tr, td, i;
        input = document.getElementById("filtro");
        filter = input.value.toUpperCase();
        table = document.getElementById("data");
        tr = table.getElementsByTagName("tr");

        // Loop through all table rows, and hide those who don't match the search query
        for (i = 0; i < tr.length; i++) {
            td1 = tr[i].getElementsByTagName("td")[1];
            td2 = tr[i].getElementsByTagName("td")[2];
            td9 = tr[i].getElementsByTagName("td")[9];
            if (td1) {
                if (td1.innerHTML.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                } else {
                    //tr[i].style.display = "none";
                    if (td2) {
                        if (td2.innerHTML.toUpperCase().indexOf(filter) > -1) {
                            tr[i].style.display = "";
                        } else {
                            //tr[i].style.display = "none";
                            if (td9) {
                                if (td9.innerHTML.toUpperCase().indexOf(filter) > -1) {
                                    tr[i].style.display = "";
                                } else {
                                    tr[i].style.display = "none";
                                }
                            }
                        }
                    }
                }
            }
        }
        }
    </script>
</body>

</html>
