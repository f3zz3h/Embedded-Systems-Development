	<!DOCTYPE html>
<meta charset="UTF-8">
<?php session_start(); ?>
<html>
<head>
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
						<h1>Museum Portal Add Device</h1>
						<br />
						<form action=\"createDevice.php\" method=\"post\" enctype=\"multipart/form-data\">
							<div class=\"form-group\">
								<label>Device Name</label>
								</br>
								<input class=\"form-control\" type=\"textbox\" name=\"deviceName\" required=\"required\"/>
								</br>
								<input type=\"submit\" class=\"btn btn-primary\" />	
							</div>
						</form>";
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