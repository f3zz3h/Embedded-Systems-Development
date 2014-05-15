<meta charset="UTF-8">
<?php session_start(); ?>
<html>
<head>
<!-- createGroup.php - The page used to create a group in the system-->
<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css" />
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
	<body>
    <div class="jumbotron narrow">
	<?php
		//Check access
		if (isset($_SESSION["CanView"]))
		{
			if ($_SESSION["CanView"] == true)
			{
				$connection = mysqli_connect("eu-cdbr-azure-west-a.cloudapp.net", "bea59dbc864a3e", "6d5abbdc", "museum", "3306");
				
				//SQl to fetch the languages we support
				$sql = "SELECT DISTINCT language from audio_file";
				$result = mysqli_query($connection, $sql);
				
				echo "<a class=\"homeLink\" href=\"/portalHome.php\"><span class=\"glyphicon glyphicon-home\"></span></a>
				<h1>Museum handset PIN portal</h1>
				<p class=\"lead subHeading\">Use this portal to create a group.</p>
				<div class=\"imgHolder wobble rotateIn\">
					<img src=\"pixel-museum.gif\" style=\"width:220px; margin-bottom:20px;\"/>
				</div>

				  <form action=\"group.php\" method=\"post\">
						<label>Language:</label>
						<select class=\"form-control\" name=\"language\" required=\"required\">";
								//Display all available languages in a select list
								while($row = mysqli_fetch_array($result))
								{
									echo "<option>".$row[0]."</option>";
								}
						echo "
						</select><br/>
						<label>Competence level:</label>
						<select class=\"form-control\" name=\"knowledge\" required=\"required\">";
								//SQL to select the available difficulties
								$sql = "SELECT DISTINCT difficulty from audio_file";
								$result = mysqli_query($connection, $sql);

								//Display all available difficulties in a select list
								while ($row = mysqli_fetch_array($result))
								{
									echo "<option>".$row[0]."</option>";
								}
						echo "
						</select><br/><div class=\"clear\"/>
						<input type=\"submit\" value=\"Save\" class=\"btn btn-primary\" id=\"btn\"/>";
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
		?>
	</div>
  </body>
</html>