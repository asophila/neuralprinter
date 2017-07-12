<?php 

if (substr_count($_SERVER['HTTP_ACCEPT_ENCODING'], 'gzip')) ob_start("ob_gzhandler"); else ob_start();

?>

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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.99.0/css/materialize.min.css">
    <link href="css/less-space.min.css" rel="stylesheet" type="text/css">
    <link type="text/css" rel="stylesheet" href="css/practia.css" media="screen,projection" />
    <style>
        .slider .slides li img {
            background-size: contain;
            background-repeat: no-repeat;
        }
        h5 {
            background-color: rgba(0,0,0, 0.5);
            border-radius: 5px;
            padding: 20px;
            color: white;
        }
        .slider .slides {
            background-color: #FFFFFF;
        }
        .slider .slides li .caption {
            top: 0;
        }
        .slider .indicators .indicator-item.active {
            background-color: #CE2021;
        }

        @media only screen and (max-width: 600px){
            .slider.landscape {
                height: 240px !important;
            }
            .slides.landscape {
                height: 200px !important;
            }
        }
    </style>
    <!-- endinject -->
</head>

<body>
    <header>
        <div class="navbar-fixed">
            <nav>
                <div class="nav-wrapper z-depth-1">
                    <a href="./" class="brand-logo left"><img src="images/logo.png" alt="Practia" class="responsive-img"></a>
                </div>
            </nav>
        </div>
    </header>
    <main>
        <div class="row">
            <div class="col s12">
                <h4>Ejemplo Retrato</h4>
                <div class="slider">
                    <ul class="slides">
                        <li>
                            <img src="./images/demo/portrait.jpg">
                            <div class="caption center-align">
                                <h5>Original</h5>
                            </div>
                        </li>
                        <li>
                            <img src="./images/demo/portrait_mosaic.jpg">
                            <div class="caption center-align">
                                <h5>Mosaic</h5>
                            </div>
                        </li>
                        <li>
                            <img src="./images/demo/portrait_candy.jpg">
                            <div class="caption center-align">
                                <h5>Candy</h5>
                            </div>
                        </li>
                        <li>
                            <img src="./images/demo/portrait_udnie.jpg">
                            <div class="caption center-align">
                                <h5>Udnie</h5>
                            </div>
                        </li>
                        <li>
                            <img src="./images/demo/portrait_starry-night.jpg">
                            <div class="caption center-align">
                                <h5>Starry night</h5>
                            </div>
                        </li>
                        <li>
                            <img src="./images/demo/portrait_van-gogh.jpg">
                            <div class="caption center-align">
                                <h5>van Gogh</h5>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col s12">
                <h4>Ejemplo Paisaje</h4>
                <div class="slider landscape">
                    <ul class="slides landscape">
                        <li>
                            <img src="./images/demo/ny.jpg">
                            <div class="caption center-align">
                                <h5>Original</h5>
                            </div>
                        </li>
                        <li>
                            <img src="./images/demo/ny_mosaic.jpg">
                            <div class="caption center-align">
                                <h5>Mosaic</h5>
                            </div>
                        </li>
                        <li>
                            <img src="./images/demo/ny_candy.jpg">
                            <div class="caption center-align">
                                <h5>Candy</h5>
                            </div>
                        </li>
                        <li>
                            <img src="./images/demo/ny_udnie.jpg">
                            <div class="caption center-align">
                                <h5>Udnie</h5>
                            </div>
                        </li>
                        <li>
                            <img src="./images/demo/ny_starry-night.jpg">
                            <div class="caption center-align">
                                <h5>Starry night</h5>
                            </div>
                        </li>
                        <li>
                            <img src="./images/demo/ny_van-gogh.jpg">
                            <div class="caption center-align">
                                <h5>van Gogh</h5>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </main>
    <footer> </footer>
    <div class="overlay fixed hide"></div>
    <!-- inject:css -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.99.0/js/materialize.min.js"></script>
    <script type="text/javascript" src="js/practia.js"></script>
    <script>
        $(document).ready(function () {
            $('.slider').slider();
        });
    </script>
    <!-- endinject -->
</body>

</html>
