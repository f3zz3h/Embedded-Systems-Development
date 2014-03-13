<!DOCTYPE html>
<meta charset="UTF-8">
<?php session_start(); ?>
<html>
<head>
<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css" />
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
	<body>
    <div class="jumbotron userManagement">
		<?php
			if (isset($_SESSION["CanView"]))
			{
				if ($_SESSION["CanView"] == true)
				{
					echo "<a class=\"homeLink\" href=\"/portalHome.php\"><span class=\"glyphicon glyphicon-home\"></span></a>
					<h1>Museum Portal User Management</h1>
					<br/>
					<a href=\"/createGroup.php\"><button type=\"button\" class=\"btn btn-primary\">Create Group</button></a>
					<br/>
					<br/>
					<a href=\"/createCustomer.php\"><button type=\"button\" class=\"btn btn-primary\">Create Customer</button></a>
					<br/>
					<br/>
					<a href=\"/manageUsers.php\"><button type=\"button\" class=\"btn btn-primary\">Manage Users</button></a>";
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