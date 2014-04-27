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
				$connection = mysqli_connect("eu-cdbr-azure-west-b.cloudapp.net", "bc39afe900a22c", "ab25d637", "museum", "3306");
				$sql = "SELECT DISTINCT language from audio_file";
				$result = mysqli_query($connection, $sql);
			
				echo "
				<a class=\"homeLink\" href=\"/portalHome.php\"><span class=\"glyphicon glyphicon-home\"></span></a>
				<h1>Museum handset PIN portal</h1>
				<p class=\"lead subHeading\">Use this portal to give up your card details so they can be stored unprotected in a text file on our server.</p>
				<div class=\"imgHolder wobble rotateIn\">
					<img src=\"pixel-museum.gif\" style=\"width:220px; margin-bottom:20px;\"/>
				</div>

				  <form action=\"customer.php\" method=\"post\">
					  <div class=\"form-group\">
						<label>Name:</label><input class=\"form-control\" type=\"text\" name=\"name\" required=\"required\"/><br/>
						<label>Address:</label><input class=\"form-control\" type=\"text\" name=\"address\" required=\"required\"/><br/>
						<label>Mobile #:</label><input class=\"form-control\" type=\"text\" name=\"mobileNumber\" required=\"required\"/><br/>
						<label>Group:</label>
						<input class=\"form-control\" type=\"text\" name=\"groupPin\" required=\"required\"/></br>
						<label>Payment card number:</label><input class=\"form-control\" id=\"CardNumber\" name=\"cardNumber\" type=\"text\" /><br/>
						<div class=\"clear\"/>
						<input type=\"submit\" value=\"Save\" class=\"btn btn-primary\" id=\"btn\"/>
					</div>
				</form>";
			}
			else
			{
				echo "<p style=\"color:red;\"><b>You do not have permission to access this page.";
			}	
		}
		else
		{
			echo "<p style=\"color:red;\"><b>You do not have permission to access this page.";
		}
		
		mysqli_close($connection);
		?>
	</div>
  </body>
</html>