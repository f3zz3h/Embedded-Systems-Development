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

						// The new person to add to the file
						$name = $_POST["name"];
						$address = $_POST["address"];
						$number = $_POST["mobileNumber"];
						$cardNumber = $_POST["cardNumber"];
						$groupPin = $_POST["groupPin"];
						
						$recordCreated = false;

						$encryptionMethod = 'aes128';
						$password = 'ESD';
						$encryptedCardNumber = openssl_encrypt($cardNumber, $encryptionMethod, $password);

						$connection = mysqli_connect("eu-cdbr-azure-west-b.cloudapp.net", "bc39afe900a22c", "ab25d637", "museum", "3306");
						
						$sql = "SELECT id FROM `group` where PIN = $groupPin";
						$result = mysqli_query($connection, $sql);
						
						$val = mysqli_fetch_array($result);

						if (!empty($val[0]))
						{						
							
							$sql = "INSERT INTO customer (name, phone, address, cardNumber, group_id)
									VALUES ('$name', '$address', '$number', '$encryptedCardNumber', $val[0])";
									
									
							if (mysqli_query($connection, $sql))
							{
								echo "<p>Customer created.</p>";
							}
						}
						else
						{
							echo "No group found with a PIN of: $groupPin";
						}
						
						mysqli_close($connection);
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

