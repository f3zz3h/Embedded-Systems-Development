<!DOCTYPE html>
<meta charset="UTF-8">
<html>
<head>
	<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css">
</head>
<body>
<?php
// the file to write too
$file = 'customers.txt';

// The new person to add to the file
$name = $_POST["name"];
$address = $_POST["address"];
$number = $_POST["mobileNumber"];
$language = $_POST["language"];
$knowledge = $_POST["knowledge"];
$cardNumber = $_POST["cardNumber"];
$pin = rand(1000,9999);
$recordCreated = false;

$encryptionMethod = 'aes128';
$password = 'ESD';
$encryptedCardNumber = openssl_encrypt($cardNumber, $encryptionMethod, $password);

// Write the contents to the file, 
// using the FILE_APPEND flag to append the content to the end of the file
// and the LOCK_EX flag to prevent anyone else writing to the file at the same time
if (isset($name, $address, $number, $language, $knowledge) && !empty($cardNumber)){
	file_put_contents($file, "$name, $address, $number, $language, $knowledge, $encryptedCardNumber, $pin \r\n", FILE_APPEND);
	$recordCreated = true;
}

if ($recordCreated == true)
{
	echo "<p>Thankyou <b>".$name."</b> your unique PIN to be entered on the device is: <b>".$pin."<b><p>";
}
else
{
	echo "<p>Something went wrong.</p>";
}

?>
</body>
</html>

