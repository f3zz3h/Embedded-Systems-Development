<!DOCTYPE html>
<meta charset="UTF-8">
<?php session_start(); ?>
<html>
<head>
<!-- manageDevices.php - Renders a table displaying current devices in the system and their availability-->
<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css" />
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
	<body>
    <div class="jumbotron narrow">
	<?php
		if (isset($_SESSION["CanView"]))
		{
			if ($_SESSION["CanView"] == true)
			{
				echo "<a class=\"homeLink\" href=\"/portalHome.php\"><span class=\"glyphicon glyphicon-home\"></span></a>
				<h1>Museum portal manage devices</h1>
				<br/>";
			
				$con = mysqli_connect("eu-cdbr-azure-west-a.cloudapp.net", "bea59dbc864a3e", "6d5abbdc", "museum", "3306");
				// Check connection
				if (mysqli_connect_errno())
				{
				echo "Failed to connect to MySQL: " . mysqli_connect_error();
				}

				$result = mysqli_query($con,"SELECT * FROM device");

				//Create our device table.
				echo "<table class=\"table table-striped\">";
				echo "<thead><th>Name</th><th>Available</th><th>Group ID</th></thead>";
				echo "<tbody>";
				
				while($row = mysqli_fetch_array($result))
				{
					//If the device is not in use, display a tick. Otherwise a cross.
					if ($row[2] == 0)
					{
						echo "<tr><td>$row[1]</td><td><span style=\"color:green\" class=\"glyphicon glyphicon-ok-sign\"</span></td><td>$row[3]</td></tr>";
					}
					else
					{
						echo "<tr><td>$row[1]</td><td><span style=\"color:red\" class=\"glyphicon glyphicon-remove-sign\"</span></td><td>$row[3]</td></tr>";
					}
				}

				echo "</tbody></table>";
				
				mysqli_close($con);
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