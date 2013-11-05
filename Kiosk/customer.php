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
$pin = rand(1000,9999);

// Write the contents to the file, 
// using the FILE_APPEND flag to append the content to the end of the file
// and the LOCK_EX flag to prevent anyone else writing to the file at the same time
file_put_contents($file, "$name, $address, $number, $language, $pin \r\n", FILE_APPEND | LOCK_EX);
?>

<p>Thankyou <b><?php echo $_POST["name"]; ?></b> your unique PIN to be entered on the device is: <b><?php echo $pin ?><b><p>

</body>
</html>

