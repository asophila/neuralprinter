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

<?php

include 'db.php';
include 'codes.php';

$uploadMessage = '';
$uploadOk = 1;
$showMessage = false;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $showMessage = true;

    $usuario = $_POST["usuario"];
    $correo = $_POST["correo"];
    $empresa = $_POST["empresa"];
    $cargo = $_POST["cargo"];
    $codigo = $_POST["codigo"];
    $estilo = $_POST["estilo"];


    #validar codigo
    $code_valid = json_decode(valid_code($codigo), true);
    if(!$code_valid['valid']){
        $uploadMessage = $code_valid['message'];
        $uploadOk = 0;
        $codigo = '';
    } else {
        $target_dir = "uploads/";
        $target_file = $target_dir . basename($_FILES["imagen"]["name"]);
        $imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);

        // Check if file already exists
        /*
        if (file_exists($target_file)) {
            $uploadMessage =  "Sorry, file already exists.";
            $uploadOk = 0;
        }
        // Check file size
        else */
        //if ($_FILES["imagen"]["size"] > 700000) {
        //    $uploadMessage = "La imagen es muy grande, intenta subir otra.";
        //   $uploadOk = 0;
        //}
        // Allow certain file formats
        //else
        if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg") {
            $uploadMessage = "Sube una imagen JPG, JPEG o PNG.";
            $uploadOk = 0;
        }
        // if everything is ok, try to upload file
        else {
            if (move_uploaded_file($_FILES["imagen"]["tmp_name"], $target_file)) {
                $uploadMessage = "Se ha enviado tu imagen \"". basename( $_FILES["imagen"]["name"]). "\"";    

                //guardar imagen en BD
                $image = addslashes(file_get_contents($target_file)); //SQL Injection defence!
                $name = pathinfo(basename( $_FILES["imagen"]["name"]), PATHINFO_FILENAME);
                $ext = '.' . pathinfo(basename( $_FILES["imagen"]["name"]), PATHINFO_EXTENSION);
                $sql = "INSERT INTO `image` (`usuario`, `ip`, `correo`, `empresa`, `cargo`, `estilo`, `name`, `ext`, `imagen`, `status`)
                                    VALUES ('$usuario', '', '$correo', '$empresa', '$cargo', '$estilo', '$name', '$ext', '$image', 'A_PROCESAR')";
                $conn = get_conn();
                if ($conn->query($sql) === TRUE) {
                    $last_id = $conn->insert_id;
                    if($codigo != 'test' and $codigo != 'IDangs'){
                        $sql = "UPDATE `code` SET `status` = 1, `image_id` = $last_id WHERE `key` = '$codigo'";
                        $conn->query($sql);
                    }
                    $uploadMessage = "Se ha enviado tu imagen \"". basename( $_FILES["imagen"]["name"]). "\""; 
                } else {
                    $uploadMessage = "No se pudo guardar tu imagen";
                    $uploadOk = 0;
                }
                $conn->close();
            } else {
                $uploadMessage = "No se pudo guardar tu imagen";
                $uploadOk = 0;
            }
            
        }
    }
}

?>

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
        <div class="row xs-pl-20 xs-pr-20<?php if(!$showMessage){ echo ' hide'; } ?>">
            <div class="col s12">
                <h5<?php if($uploadOk){ echo ''; } else { echo ' class="error"'; } ?>><?php echo $uploadMessage; ?></h5>
            </div>
        </div>
        <div class="row xs-pl-20 xs-pr-20">
            <div class="col s12">
                <h5>¿Qué son las REDES NEURONALES?</h5>
                <p>Las <b>Redes Neuronales Artificiales</b> imitan el funcionamiento del cerebro humano en un computador. Integrando
                    sistemas simples, llamados perceptrones, es posible construir aplicaciones complejas tales como comprender
                    el lenguaje; identificar los objetos en imágenes o videos y clasificar documentos.</p>
                <p><b>En Practia entrenamos nuestra red neuronal, para que pinte tu imagen aplicando el estilo artístico que elijas.</b></p>
            </div>
        </div>
        <div class="row">
            <form id="form-file" class="col s12" action="./" method="post" enctype="multipart/form-data">
                <div class="row">
                    <div class="input-field col s12"> <input name="usuario" id="usuario" type="text" class="validate" required> <label for="usuario">* Nombre</label></div>
                    <div class="input-field col s12"> <input name="correo" id="correo" type="email" class="validate" required> <label for="correo" data-error="Correo no válido">* Correo</label>                        </div>
                </div>
                <div class="row">
                    <div class="input-field col s12"> <input name="empresa" id="empresa" type="text" class="validate" required> <label for="empresa">* Empresa</label></div>
                    <div class="input-field col s12"> <input name="cargo" id="cargo" type="text" class="validate" required> <label for="cargo">* Cargo</label>                        </div>
                </div>
                <div class="row">
                    <div class="input-field col s12"> <input name="codigo" id="codigo" type="text" class="validate" required> <label for="codigo">* Código</label></div>
                </div>
                <div class="row">
                    <div class="input-field col s4 push-s8"> <select name="estilo" class="icons" required>
                            <option value="" disabled selected>Selecciona un estilo</option>
                            <option value="mosaic" data-icon="images/styles/mosaic.jpg" class="left circle">Mosaico</option>
                            <option value="candy" data-icon="images/styles/candy.jpg" class="left circle">Candy</option>
                            <option value="udnie" data-icon="images/styles/udnie.jpg" class="left circle">Udnie</option>
                            <option value="starry-night" data-icon="images/styles/starry-night.jpg" class="left circle">Starry Night</option>
                        </select> <label>* Estilo</label> </div>
                    <div class="file-field input-field col s8 pull-s4">
                        <div class="btn"><i class="material-icons left">perm_media</i><span>Imagen</span> <input name="imagen" type="file"
                                required> </div>
                        <div class="file-path-wrapper"> <input class="file-path" type="text"> </div>
                    </div>
                </div>
                <div class="row center-align"> <button class="btn waves-effect waves-light btn-large" type="submit" name="action">Enviar<i class="material-icons right">send</i></button>                    </div>
            </form>
        </div>
    </main>
    <footer> </footer>
    <div class="overlay fixed hide"></div>
    <!-- inject:css -->
    <script type="text/javascript" src="js/jquery.min.js"></script>
    <script type="text/javascript" src="js/materialize.min.js"></script>
    <script type="text/javascript" src="js/practia.js"></script>
    <script>
        $(document).ready(function () {
        <?php
            if(!$uploadOk){
                if (isset($usuario)) {
                    echo "$('#usuario').val('" . $usuario ."');";
                }
                if (isset($correo)) {
                    echo "$('#correo').val('" . $correo ."');";
                }
                if (isset($empresa)) {
                    echo "$('#empresa').val('" . $empresa ."');";
                }
                if (isset($cargo)) {
                    echo "$('#cargo').val('" . $cargo ."');";
                }
                if (isset($codigo)) {
                    echo "$('#codigo').val('" . $codigo ."');";
                }
                echo 'Materialize.updateTextFields();';
            }
        ?>
        $('select').material_select();

        // for HTML5 "required" attribute
        $("select[required]").css({ display: "block", height: 0, padding: 0, margin: "0 60px", width: 0, position: "relative", top: "-18px" });
        $(".file-field > .btn input[type=file]").css({ bottom: "18px" });
    });
    </script>
    <!-- endinject -->
</body>

</html>
