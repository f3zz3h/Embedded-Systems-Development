<!DOCTYPE html>
<meta charset="UTF-8">
<?php session_start(); ?>
<html>
<head>
<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css" />
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
	<body>
    <div class="jumbotron manageUsers">
	<?php
		if (isset($_SESSION["CanView"]))
		{
			if ($_SESSION["CanView"] == true)
			{
				echo "<a class=\"homeLink\" href=\"/portalHome.php\"><span class=\"glyphicon glyphicon-home\"></span></a>
				<h1>Museum portal manage users</h1>
				<br/>";
			
				$con = mysqli_connect("eu-cdbr-azure-west-b.cloudapp.net:3306", "bc39afe900a22c", "ab25d637", "museum");
				// Check connection
				if (mysqli_connect_errno())
				{
				echo "Failed to connect to MySQL: " . mysqli_connect_error();
				}

				$result = mysqli_query($con,"SELECT * FROM customer");

				echo "<table class=\"table table-striped\">";
				echo "<thead><th>Name</th><th>Phone #</th><th>Address</th><th>Language</th><th>Competence</th><th>Edit</th><th>Delete</th></thead>";
				echo "<tbody>";
				
				while($row = mysqli_fetch_array($result))
				{
					echo "<tr><td>$row[1]</td><td>$row[2]</td><td>$row[3]</td><td>$row[4]</td><td>$row[5]</td><td><a href=\"/updateCustomer.php?id=$row[0]\"><span class=\"glyphicon glyphicon-cog\"></span></a></td><td><a href=\"/deleteCustomer.php?id=$row[0]\"><span class=\"glyphicon glyphicon-remove\"></span></a></td></tr>";
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