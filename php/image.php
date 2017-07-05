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
    <header>
        <div class="navbar-fixed">
            <nav>
                <div class="nav-wrapper z-depth-1"> <a href="./" class="brand-logo left"><img src="images/logo.png" alt="Practia" class="responsive-img"></a>                    </div>
                <div class="progress-bar">
                    <div class="progress z-depth-1 hide">
                        <div class="indeterminate"></div>
                    </div>
                </div>
            </nav>
        </div>
    </header>
    <main>
            <?php
                include 'db.php';

                if (isset($_GET['correo'])){
                    $conn = get_conn();
                    $sql = "SELECT * FROM `image` WHERE `correo` = '" . $_GET['correo'] . "' ORDER BY `id` DESC LIMIT 1";
                    $result = $conn->query($sql);

                    while ( $row = mysqli_fetch_array($result))
                    {
                        echo '<div class="row xs-p-20 z-depth-2">';

                        echo '<div class="col s12 m6"><p>Imagen <b>"' . $row['name'] . $row['ext'] . '"</b></p>';
                        echo '<img class="responsive-img" src="data:image/jpeg;base64,'.base64_encode( $row['imagen'] ).'"/></div>';

                        if( $row['imagen_style']){
                            echo '<div class="col s12 m6"><p>Estilo <b>"' . $row['estilo'] . '"</b></p>';
                            echo '<img class="responsive-img" src="data:image/jpeg;base64,'.base64_encode( $row['imagen_style'] ).'"/></div>';
                        } else {
                            echo '<div class="col s12 m6"><p>Estilo ' . $row['estilo'] . '</p><p><b>Procesando imagen, intenta en un momento...</b></p></div>';
                        }
                        echo '</div>';
                    }

                    $conn->close();
                }
            ?>
    </main>
    <footer> </footer>
    <div class="overlay fixed hide"></div>
    <!-- inject:css -->
    <script type="text/javascript" src="js/jquery.min.js"></script>
    <script type="text/javascript" src="js/materialize.min.js"></script>
    <script type="text/javascript" src="js/practia.js"></script>
    <!-- endinject -->
</body>

</html>
