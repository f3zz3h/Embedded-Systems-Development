<!DOCTYPE html>
<meta charset="UTF-8">
<?php session_start(); ?>
<html>
	<head>
		<!-- ManageUsers.php - Renders a table displaying current customers and provides management options-->
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
						echo "<a class=\"homeLink\" href=\"/portalHome.php\"><span class=\"glyphicon glyphicon-home\"></span></a>";
			
						$deviceName = $_POST["deviceName"];
						
						$connection = mysqli_connect("eu-cdbr-azure-west-b.cloudapp.net", "bc39afe900a22c", "ab25d637", "museum", "3306");
						
						$sql = "INSERT INTO device (name, inUse) VALUES ('$deviceName', 0)";
						
						if (mysqli_query($connection, $sql))
						{
							echo "<p>Device created.</p>";
						}
						else
						{
							echo mysqli_error();
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

