<!DOCTYPE html>
<meta charset="UTF-8">
<?php session_start(); ?>
<html>
<head>
<!-- portalHome.php - Home page of the Kiosk portal-->
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
					echo "<h1>Museum Portal Index</h1>
					<a href=\"/userManagement.php\"><button type=\"button\" class=\"btn btn-primary\">Manage Users</button></a>
					<br/>
					<br/>
					<a href=\"/fileManagement.php\"><button type=\"button\" class=\"btn btn-primary\">Manage Files</button></a>
					<br/>
					<br/>
					<a href=\"/deviceManagement.php\"><button type=\"button\" class=\"btn btn-primary\">Manage Devices</button></a>";
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