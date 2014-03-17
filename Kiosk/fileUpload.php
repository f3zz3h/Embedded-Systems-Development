<!DOCTYPE html>
<meta charset="UTF-8">
<?php session_start(); ?>
<html>
	<head>
		<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css">
		<link rel="stylesheet" type="text/css" href="style.css">
	</head>
	<body>
		<div class="jumbotron fileUpload">
			<?php
				if (isset($_SESSION["CanView"]))
				{
					if ($_SESSION["CanView"] == true)
					{
						echo "<a class=\"homeLink\" href=\"/portalHome.php\"><span class=\"glyphicon glyphicon-home\"></span></a>";
			
			
						$allowedExts = "mp3";
						$temp = explode(".", $_FILES["file"]["name"]);
						$extension = end($temp);
						$language = $_POST["language"];
						$difficulty = $_POST["difficulty"];
						
						$connection = mysqli_connect("eu-cdbr-azure-west-b.cloudapp.net:3306", "bc39afe900a22c", "ab25d637", "museum");
						
						if (isset($_FILES) && $extension == $allowedExts)
						{	
							if ($_FILES["file"]["error"] > 0)
							{
								echo "Error: " . $_FILES["file"]["error"] . "<br>";
							}
							else
							{
								echo "Upload: " . $_FILES["file"]["name"] . "<br>";
								echo "Type: " . $_FILES["file"]["type"] . "<br>";
								echo "Size: " . round(($_FILES["file"]["size"] / 1024)) . " kB<br>";
								
								$saveLocation = "\\audio\\";
								
								if (move_uploaded_file($_FILES["file"]["tmp_name"], $saveLocation))
								{
									echo "<br/><p>Stored in: $saveLocation";
								}
								
								if (mysqli_connect_errno())
								{
									echo "<p>Failed to conect to MySQL: " . mysqli_connect_error() . "</p>";
								}
								
								$saveLocation = $city = mysqli_real_escape_string($connection, $saveLocation);
								
								if (isset($language, $difficulty))
								{
									$sql = "INSERT INTO audio_file (language, difficulty, dir)
											VALUES ('$language', '$difficulty', '$saveLocation')";
								
									if (mysqli_query($connection, $sql))
									{
										echo "<p>Database entry created.</p>";
									}
									else
									{
										echo "<p>" . mysqli_error($connection) . "</p>";
									}
								}
							}
						}
						else
						{
							echo "<p>Please upload a valid audio file.</p>";
						}
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

