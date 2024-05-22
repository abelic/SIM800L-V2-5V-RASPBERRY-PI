<?php
// Definišite vaš Bearer token ovde
$valid_bearer_token = "17|XEd7e9ofeb3Kgn82DHzeH2NFDLakY3Vwv3fr5eXL";

// Dobijanje Bearer tokena iz Authorization header-a
$headers = apache_request_headers();
$auth_header = isset($headers['Authorization']) ? $headers['Authorization'] : '';

if (preg_match('/Bearer\s(\S+)/', $auth_header, $matches)) {
    $bearer_token = $matches[1];
} else {
    http_response_code(401);
    echo json_encode(["message" => "Unauthorized: No Bearer token found"]);
    exit;
}

if ($bearer_token !== $valid_bearer_token) {
    http_response_code(401);
    echo json_encode(["message" => "Unauthorized: Invalid Bearer token"]);
    exit;
}

$data = json_decode(file_get_contents('php://input'), true);

if (!isset($data['number']) || !isset($data['message'])) {
    http_response_code(400);
    echo json_encode(["message" => "Bad Request: 'number' and 'message' parameters are required"]);
    exit;
}

$number = $data['number'];
$message = $data['message'];

$escaped_number = escapeshellarg($number);
$escaped_message = escapeshellarg($message);
$command = "python3 send_sms.py $escaped_number $escaped_message > /dev/null 2>&1 &";
exec($command);

http_response_code(200);
echo json_encode(["message" => "Request received. SMS will be sent shortly."]);
?>
