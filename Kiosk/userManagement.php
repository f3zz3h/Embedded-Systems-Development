<!DOCTYPE html>
<meta charset="UTF-8">
<?php 
//Start the session to allow use of the session variables.
session_start(); 
?>
<html>
<head>
<!-- userManagement.php - User management page, either create a group or customer, or manage customers-->
<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css" />
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
	<body>
    <div class="jumbotron narrow">
		<?php
			//Check to see if the session variable has been set.
			if (isset($_SESSION["CanView"]))
			{
				//If user can view the page, render the HTML.
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