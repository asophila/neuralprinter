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
    <style>
        .slider .slides li img {
            background-size: contain;
            background-repeat: no-repeat;
        }
        h3, h5 {
            background-color: rgba(0,0,0, 0.5);
            border-radius: 5px;
            padding: 20px;
            color: white;
        }
        .slider .slides,
        .slider .indicators .indicator-item.active {
            background-color: #CE2021;
        }
        .logo {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: auto;
            z-index: 9999;
            padding: 10px;
            background-color: rgba(0,0,0,0.3);
        }
    </style>
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
            <?php
                include 'db.php';

                $correo = null;
                if (isset($_GET['correo'])){
                    $correo = $_GET['correo'];
                } else if (isset($_POST['correo'])){
                    $correo = $_POST['correo'];
                }

                if ($correo){
                    $procesando = 0;
                    $procesado = 0;

                    $conn = get_conn();
                    $sql = "SELECT * FROM `image` WHERE `correo` = '" . $correo . "' ORDER BY `id` DESC";
                    $result = $conn->query($sql);

                    while ( $row = mysqli_fetch_array($result))
                    {
                        if( $row['imagen_style']){
                            if($procesado < 1){
                                echo '<div class="slider fullscreen"><ul class="slides">';
                            }
                            echo '<li>';
                            echo '<img src="data:image/jpeg;base64,'.base64_encode( $row['imagen_style'] ).'"/>';
                            echo '<div class="caption center-align">';

                            echo '<h3>';
                            echo $row['estilo'];
                            echo '</h3>';

                            echo '</div>';
                            echo '</li>';
                            $procesado += 1;
                        } else {
                            $procesando += 1;
                        }
                    }

                    if($procesado > 0){
                            echo '</ul></div>';
                        }
                    $conn->close();
                
    if($procesado < 1 and $procesando < 1) { ?>
    <header>
        <div class="navbar-fixed">
        <nav>
            <div class="nav-wrapper z-depth-1"> <a href="./" class="brand-logo"><img src="images/logo.png" alt="Practia" class="responsive-img" ></a> </div>
        </nav>
        </div>
    </header>
    <main>
        <div class="row xs-pl-20 xs-pr-20">
            <div class="col s12 center">
                <h5>No tenemos imágenes para procesar para tu correo.<br>Completa nuestro formulario</h5>
            </div>
        </div>
        <div class="row center-align"> <a href="./" class="waves-effect waves-light btn-large"><i class="material-icons left">home</i>Ir al formulario</a> </div>
    </main>
    <footer> </footer>
    <?php
     } else {
    ?>
    <div class="logo center">
        <a href="./imagenes.php" class="brand-logo left"><img src="images/logo.png" alt="Practia" class="responsive-img"></a>
        <?php 
            if($procesando > 0){
                echo '<a href="'.$_SERVER['REQUEST_URI'].'" class="white-text">Nos falta';
                if($procesando > 1){ echo 'n ';} else { echo ' '; } 
                echo $procesando;
                if($procesando > 1){ echo ' imágenes ';} else { echo ' imagen '; }
                echo ' por procesar, intenta nuevamente en un momento para revisarlas</a>';
            }
        ?>
    </div>
     <?php }

                } else {
     
     ?>
     <header>
        <div class="navbar-fixed">
        <nav>
            <div class="nav-wrapper z-depth-1"> <a href="./" class="brand-logo"><img src="images/logo.png" alt="Practia" class="responsive-img" ></a> </div>
        </nav>
        </div>
    </header>
    <main>
     <div class="row xs-pl-20 xs-pr-20 center">
            <h5>Ingresa el correo que usaste en nuestro formulario para ver tus imágenes procesadas</h5>
            <form id="form-file" class="col s12" action="./imagenes.php" method="post" enctype="multipart/form-data">
                <div class="row center-align">
                    <div class="input-field col s12"> <input name="correo" id="correo" type="email" class="validate" required> <label for="correo" data-error="Correo no válido">* Correo</label>                        </div>
                </div>
                <div class="row center-align"> <button class="btn waves-effect waves-light btn-large" type="submit" name="action"><i class="material-icons right">photo_library</i>Ver mis imágenes</button></div>
            </form>
        </div>
        </main>
    <footer> </footer>
                <?php } ?>


    <!-- inject:css -->
    <script type="text/javascript" src="js/jquery.min.js"></script>
    <script type="text/javascript" src="js/materialize.min.js"></script>
    <script type="text/javascript" src="js/practia.js"></script>
    <script>
        $(document).ready(function(){
            $('.slider').slider();

            setTimeout(function() {
                $("body").addClass("loaded");
            }, 200);
        });

        $( "#form-file" ).submit(function( event ) {
            setTimeout(function() {
                $("body").removeClass("loaded");
            }, 200);
        });
    </script>
    <!-- endinject -->
</body>

</html>
