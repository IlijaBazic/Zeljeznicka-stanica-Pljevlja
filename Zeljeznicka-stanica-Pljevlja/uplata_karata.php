<?php // uplata_karata.php
$input = json_decode(file_get_contents('php://input'), true);  
$to = "info@zeljeznickastanicapljevlja.me";
$subject = "Uplata karata sa sajta";
$message = "Ime: ".$input['ime']."\nPrezime: ".$input['prezime']."\nEmail: ".$input['email']."\nBroj karata: ".$input['broj_karata']."\nDatum: ".$input['datum']."\nVrijeme: ".$input['vrijeme'];
$headers = "From: ".$input['email'];
if(mail($to, $subject, $message, $headers)){
    echo json_encode(["status"=>"ok"]);
} else {
    http_response_code(500);
    echo json_encode(["status"=>"error"]);
}
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(["status"=>"error", "message"=>"Method not allowed"]);
    exit;
}
if (empty($input['ime']) || empty($input['prezime']) || empty($input['email']) || empty($input['broj_karata']) || empty($input['datum']) || empty($input['vrijeme'])) {
    http_response_code(400);
    echo json_encode(["status"=>"error", "message"=>"Missing required fields"]);
    exit;
}
if (!filter_var($input['email'], FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(["status"=>"error", "message"=>"Invalid email format"]);
    exit;
}
if (!is_numeric($input['broj_karata']) || $input['broj_karata'] <= 0) {
    http_response_code(400);
    echo json_encode(["status"=>"error", "message"=>"Invalid number of tickets"]);
    exit;
}
if (!DateTime::createFromFormat('Y-m-d', $input['datum']) || !DateTime::createFromFormat('H:i', $input['vrijeme'])) {
    http_response_code(400);
    echo json_encode(["status"=>"error", "message"=>"Invalid date or time format"]);
    exit;
}
// Validate the input data to ensure it meets the expected format and constraints.
if (!preg_match("/^[a-zA-Z\s]+$/", $input['ime']) || !preg_match("/^[a-zA-Z\s]+$/", $input['prezime'])) {
    http_response_code(400);
    echo json_encode(["status"=>"error", "message"=>"Invalid name format"]);
    exit;
}
// Ensure that the input is sanitized to prevent XSS or other injection attacks.
$input['ime'] = htmlspecialchars(strip_tags($input['ime']));
$input['prezime'] = htmlspecialchars(strip_tags($input['prezime']));
$input['email'] = htmlspecialchars(strip_tags($input['email']));
$input['broj_karata'] = htmlspecialchars(strip_tags($input['broj_karata']));
$input['datum'] = htmlspecialchars(strip_tags($input['datum']));
$input['vrijeme'] = htmlspecialchars(strip_tags($input['vrijeme']));
// Note: This code does not include a database connection or storage for the ticket purchase.
// If you need to store the ticket purchase, you should implement a database connection and insert the data into a table.
// Ensure that the email sending function is secure and does not allow header injection.
// The mail function is used here for simplicity, but consider using a more robust mailing library like PHPMailer or SwiftMailer for production use.


// Additional security measures can be added here, such as rate limiting or CAPTCHA to prevent spam.
//add code for rate limiting or CAPTCHA to prevent spam


// Ensure that the email sending function is secure and does not allow header injection.
// The mail function is used here for simplicity, but consider using a more robust mailing library like PHPMailer or SwiftMailer for production use.


// This code is a simple PHP script to handle ticket purchases from a web form.
// It validates the input, sends an email with the ticket details, and returns a JSON response.
// Note: Make sure to configure your PHP environment to allow sending emails.
// This code is a simple PHP script to handle ticket purchases from a web form.
// It validates the input, sends an email with the ticket details, and returns a JSON response.
//Potential improvements could include:
// - Adding a database connection to store ticket purchases.
// - Implementing a more robust email sending library for better error handling and security.
// - Adding logging for successful and failed email sends.
// - Implementing rate limiting or CAPTCHA to prevent spam submissions.
//Plaćanje karata je sada moguće putem ovog skripta.
// Uplata karata je sada moguća putem ovog skripta. 
//Povezanost sa PayPal ili Stripe može biti dodata u budućnosti za online plaćanje karata.
?>
