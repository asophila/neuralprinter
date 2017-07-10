<?php

function getUserIP()
{
    $client  = @$_SERVER['HTTP_CLIENT_IP'];
    $forward = @$_SERVER['HTTP_X_FORWARDED_FOR'];
    $remote  = $_SERVER['REMOTE_ADDR'];

    if(filter_var($client, FILTER_VALIDATE_IP))
    {
        $ip = $client;
    }
    elseif(filter_var($forward, FILTER_VALIDATE_IP))
    {
        $ip = $forward;
    }
    else
    {
        $ip = $remote;
    }

    return $ip;
}

function get_next_to_print($ev, $correo){
    $evento = $ev;
    if(strlen($evento) != 2 || (isset($_GET['evento']) && strlen($_GET['evento']) == 2)){
        $evento = $_GET['evento'];
    }
    if(strlen($evento) != 2){
        $response = array(
            'error' => true,
            'message' => 'Debe indicar un evento válido ["'.$evento.'"]',
            'evento' => $evento
        );
        return json_encode($response);
    }

    $conn = get_conn();
    $sql = "SELECT * FROM `image` WHERE `status` = 'PROCESADO' and `ip` = '" . $evento ."' ORDER BY `id` ASC";

    $result = $conn->query($sql);
    $response = array();
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();

        $sql_code = "SELECT * FROM `code` WHERE `image_id` = " . $row['id'];
        $result_code = $conn->query($sql_code);
        if ($result_code->num_rows > 0) {
            $code = $result_code->fetch_assoc();
            $code = $code['key'];
        } else {
            $code = '';
        }

        $response = array(
            'error' => false,
            'message' => '',
            'id' => $row['id'],
            'codigo' => $code,
            'correo' => $row['correo'],
            'name' => $row['name'] . '_'. $row['estilo'],
            'ext' => $row['ext'],
            'imagen' => base64_encode( $row['imagen_style'] ),
            'evento' => $evento,
            'body_correo' => $correo
        );
    } else {
        $response = array(
            'error' => true,
            'message' => 'No hay más por imprimir ["'.$evento.'"]',
            'evento' => $evento
        );
    }
    $conn->close();
    return json_encode($response);
}

function get_correo($evento){
    if($evento == 'CL'){
        return 'Gracias por asistir al stand de Practia en el evento Chile.<br><br>Te enviamos la imagen que fue procesada usando Redes Neuronales.<br><br>Hay miles de proyectos digitales esperando ser abordados, Practia ya está listo para ayudarte a concretarlos.<br>';
    }
    if($evento == 'AR'){
        return 'Gracias por asistir al stand de Practia en el evento Argentina.<br><br>Te enviamos la imagen que fue procesada usando Redes Neuronales.<br><br>Hay miles de proyectos digitales esperando ser abordados, Practia ya está listo para ayudarte a concretarlos.<br>';
    }
    if($evento == 'PE'){
        return 'Gracias por asistir al stand de Practia en el evento Perú.<br><br>Te enviamos la imagen que fue procesada usando Redes Neuronales.<br><br>Hay miles de proyectos digitales esperando ser abordados, Practia ya está listo para ayudarte a concretarlos.<br>';
    }
    return 'Gracias por asistir al stand de Practia.<br><br>Te enviamos la imagen que fue procesada usando Redes Neuronales.<br><br>Hay miles de proyectos digitales esperando ser abordados, Practia ya está listo para ayudarte a concretarlos.<br>';
}

header("Content-Type: application/json; charset=utf-8");
include 'db.php';



$user_ip = getUserIP();
$evento = '';
if(strlen($user_ip) > 5){
    $geo = json_decode(file_get_contents('http://www.geoplugin.net/json.gp?ip='.$user_ip));
    if($geo->geoplugin_status == 200){
        $evento = $geo->geoplugin_countryCode;
    }
}
$correo = get_correo($evento);

echo get_next_to_print($evento, $correo);

?>
