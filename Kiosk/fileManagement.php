<!DOCTYPE html>
<meta charset="UTF-8">
<?php session_start(); ?>
<html>
<head>
<!-- fileManagement.php - File management homepage, from here, view files or add a new one-->
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
						<h1>Museum Portal File Management</h1>
						<br/>
						<a href=\"/uploadFile.php\"><button type=\"button\" class=\"btn btn-primary\">Upload File</button></a>
						<br/>
						<br/>
						<a href=\"/manageFiles.php\"><button type=\"button\" class=\"btn btn-primary\">Manage Files</button></a>";
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