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
						$pin = rand(1000,9999);

						$connection = mysqli_connect("eu-cdbr-azure-west-b.cloudapp.net:3306", "bc39afe900a22c", "ab25d637", "museum");
						
						$language = $_POST["language"];
						$difficulty = $_POST["knowledge"];
						
						if (isset($language) && isset($difficulty))
						{
							$sql = "SELECT id from audio_file WHERE (language = $language AND difficulty = $difficulty)";
							$result = mysqli_query($connection, $sql);
							$row = mysqli_fetch_array($result);
							
							$audioFileId = $row[0];
							
							$sql = "INSERT INTO group (audio_file_id, PIN) VALUES ($audioFileId, $pin)";
							$result = mysqli_query($connection, $sql);
							
							mysqli_close($connection);

							if ($result)
							{
								echo "<p>Thankyou <b>".$name."</b> your unique PIN to be entered on the device is: <b>".$pin."<b><p>";
								echo "<a href=\"/createCustomer.html\"><span class=\"glyphicon glyphicon-plane\"><br/>Go to create customer page.</span>";
							}
							else
							{
								echo "<p>Something went wrong.</p>";
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

