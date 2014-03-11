<!DOCTYPE html>
<meta charset="UTF-8">
<?php session_start(); ?>
<html>
	<head>
		<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css">
		<link rel="stylesheet" type="text/css" href="style.css">
	</head>
	<body>
		<div class="jumbotron customer">
			<?php
				if (isset($_SESSION["CanView"]))
				{
					if ($_SESSION["CanView"] == true)
					{
						ini_set("display_errors", 0);
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
						$id = $_POST["id"];

						$encryptionMethod = 'aes128';
						$password = 'ESD';
						$encryptedCardNumber = openssl_encrypt($cardNumber, $encryptionMethod, $password);

						$connection = mysqli_connect("eu-cdbr-azure-west-b.cloudapp.net:3306", "bc39afe900a22c", "ab25d637", "museum");

						if (is_null($id))
						{
							$sql = "INSERT INTO customer (name, phone, address, language, competence, cardNumber)
								VALUES ('$name', '$address', '$number', '$language', '$knowledge', '$encryptedCardNumber')";
						}
						else
						{
							$sql = "UPDATE customer
									SET name = '$name', address = '$address', language = '$language', competence = '$knowledge', cardNumber = '$encryptedCardNumber'
									WHERE id = '$id'";
						}

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

						if ($recordCreated == true && is_null($id))
						{
							echo "<p>Thankyou <b>".$name."</b> your unique PIN to be entered on the device is: <b>".$pin."<b><p>";
						}
						else if ($recordCreated == true && isset($id))
						{
							echo "<p>Record updated.</p>";
							echo "<a href=\"/userManagement.html\"><span class=\"glyphicon glyphicon-plane\"><br/>Fly home!</span>";
						}
						else
						{
							echo "<p>Something went wrong.</p>";
						}
					}
					else
					{
						echo "<p style=\"color:red;\"><b>You do not have permission to view this page.</b></p>";
					}
				}
				else
				{
					echo "<p style=\"color:red;\"><b>You do not have permission to view this page.</b></p>";
				}
			?>
		</div>
	</body>
</html>

