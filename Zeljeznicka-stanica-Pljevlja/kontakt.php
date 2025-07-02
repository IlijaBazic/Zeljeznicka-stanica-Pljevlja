<?php
// kontakt.php
$input = json_decode(file_get_contents('php://input'), true);
$to = "info@zeljeznickastanicapljevlja.me";
$subject = "Kontakt poruka sa sajta";
$message = "Ime: ".$input['ime']."\nPrezime: ".$input['prezime']."\nEmail: ".$input['email']."\nPoruka: ".$input['poruka'];
$headers = "From: ".$input['email'];
if(mail($to, $subject, $message, $headers)){
    echo json_encode(["status"=>"ok"]);
} else {
    http_response_code(500);
    echo json_encode(["status"=>"error"]);
}
?>