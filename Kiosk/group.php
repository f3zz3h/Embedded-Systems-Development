<!DOCTYPE html>
<meta charset="UTF-8">
<?php session_start(); ?>
<html>
	<head>
		<!-- group.php - Handles the creation of groups in the system-->
		<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css">
		<link rel="stylesheet" type="text/css" href="style.css">
	</head>
	<body>
		<div class="jumbotron narrow">
			<?php
				if (isset($_SESSION["CanView"]))
				{
					if ($_SESSION["CanView"] == true)
					{
						//Generate a random 4 digit pin
						$pin = rand(1000,9999);

						$connection = mysqli_connect("eu-cdbr-azure-west-a.cloudapp.net", "bea59dbc864a3e", "6d5abbdc", "museum", "3306");
						
						//Fetch our group data from the POST Request
						$language = $_POST["language"];
						$difficulty = $_POST["knowledge"];
						
						if (isset($language) && isset($difficulty))
						{
							//Grab the ID of an audio file that matches a specified language and difficulty
							$sql = "SELECT id from audio_file WHERE (language = '$language' AND difficulty = '$difficulty')";
							$result = mysqli_query($connection, $sql);
							$row = mysqli_fetch_array($result);
							
							$audioFileId = $row[0];
							
							//Using this ID, create a group entry that links to the relevant audio file.
							$sql = "INSERT INTO `group` (audio_file_id, PIN) VALUES ($audioFileId, $pin)";
							$result = mysqli_query($connection, $sql);
							
							mysqli_close($connection);

							//If there is no result present we know there was no audio file for the required difficulty/language, so we error.
							//Otherwise, display the device PIN to the user
							if ($result)
							{
								echo "<p>Thankyou, your unique PIN to be entered on the device is: <b>".$pin."<b><p>";
								echo "<a href=\"/createCustomer.php\"><span class=\"glyphicon glyphicon-plane\"><br/>Go to create customer page.</span>";
							}
							else
							{
								echo "<p>Something went wrong (Possibly difficulty/language mismatch)</p>";
							}
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

