<!DOCTYPE html>
<meta charset="UTF-8">
<?php session_start(); ?>
<html>
	<head>
		<!-- customer.php - Handles creation of a customer record in the database-->
		<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css">
		<link rel="stylesheet" type="text/css" href="style.css">
	</head>
	<body>
		<div class="jumbotron narrow">
			<?php
				//Check access
				if (isset($_SESSION["CanView"]))
				{
					if ($_SESSION["CanView"] == true)
					{
						//Don't display any warnings or errors (these surround encryption, not important..)
						ini_set("display_errors", 0);

						// The new person to add to the file
						$name = $_POST["name"];
						$address = $_POST["address"];
						$number = $_POST["mobileNumber"];
						$cardNumber = $_POST["cardNumber"];
						$groupPin = $_POST["groupPin"];
						
						$recordCreated = false;

						//Encrypt our card details.
						$encryptionMethod = 'aes128';
						$password = 'ESD';
						$encryptedCardNumber = openssl_encrypt($cardNumber, $encryptionMethod, $password);

						//Create connection object
						$connection = mysqli_connect("eu-cdbr-azure-west-a.cloudapp.net", "bea59dbc864a3e", "6d5abbdc", "museum", "3306");
						
						//Make sure the group is real
						$sql = "SELECT id FROM `group` where PIN = $groupPin";
						$result = mysqli_query($connection, $sql);
						
						$val = mysqli_fetch_array($result);

						//If the group exists, add the customer to the DB
						if (!empty($val[0]))
						{						
							
							$sql = "INSERT INTO customer (name, phone, address, cardNumber, group_id)
									VALUES ('$name', '$address', '$number', '$encryptedCardNumber', $val[0])";
									
									
							if (mysqli_query($connection, $sql))
							{
								echo "<a class=\"homeLink\" href=\"/portalHome.php\"><span class=\"glyphicon glyphicon-home\"></span></a></br><p>Customer created.</p>";
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

