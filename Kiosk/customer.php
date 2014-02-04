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

$connection = mysqli_connect("localhost:3306", "root", "", "esd");
$sql = "INSERT INTO customer (name, phone, address, language, competence, cardNumber)
		VALUES ('$name', '$address', '$number', '$language', '$knowledge', '$encryptedCardNumber')";
if (mysqli_connect_errno())
{
	echo "<p>Failed to conect to MySQL: " . mysqli_connect_error() . "</p>";
}

if (isset($name, $address, $number, $language, $knowledge) && !empty($cardNumber)){
	if (mysqli_query($connection, $sql))
	{
		$recordCreated = true;
	}
	else
	{
		echo "<p>" . mysqli_error($connection) . "</p>";
	}
}

mysqli_close($connection);

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

