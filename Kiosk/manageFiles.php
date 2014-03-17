<!DOCTYPE html>
<meta charset="UTF-8">
<?php session_start(); ?>
<html>
<head>
<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css" />
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
	<body>
    <div class="jumbotron manageFiles">
	<?php
		if (isset($_SESSION["CanView"]))
		{
			if ($_SESSION["CanView"] == true)
			{
				echo "<a class=\"homeLink\" href=\"/portalHome.php\"><span class=\"glyphicon glyphicon-home\"></span></a>
				<h1>Museum portal manage files</h1>
				<br/>";
			
				$con = mysqli_connect("eu-cdbr-azure-west-b.cloudapp.net", "bc39afe900a22c", "ab25d637", "museum", "3306");
				// Check connection
				if (mysqli_connect_errno())
				{
				echo "Failed to connect to MySQL: " . mysqli_connect_error();
				}

				$result = mysqli_query($con, "SELECT * FROM audio_file");

				echo "<table class=\"table table-striped\">";
				echo "<thead><th>Language</th><th>Difficulty</th><th>Location</th><th>Delete</th></thead>";
				echo "<tbody>";
				
				while($row = mysqli_fetch_array($result))
				{
					echo "<tr><td>$row[1]</td><td>$row[2]</td><td>$row[3]</td><td><a href=\"/deleteFile.php?id=$row[0]&loc=$row[3]\"><span class=\"glyphicon glyphicon-remove\"></span></a></td></tr>";
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