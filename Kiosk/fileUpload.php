<!DOCTYPE html>
<meta charset="UTF-8">
<?php session_start(); ?>
<html>
	<head>
		<!-- fileUpload.php - Handles file uploads to the server-->
		<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css">
		<link rel="stylesheet" type="text/css" href="style.css">
	</head>
	<body>
		<div class="jumbotron narrow">
			<?php
				if (isset($_SESSION["CanView"]))
				{
					if ($_SESSION["CanView"] == true)
					{
						echo "<a class=\"homeLink\" href=\"/portalHome.php\"><span class=\"glyphicon glyphicon-home\"></span></a>";
			
			
			
						$allowedExts = "mp3";
						$temp = explode(".", $_FILES["file"]["name"]); //Split our filename into two parts from at the '.'
						$extension = end($temp); //Our extension is the end of the explosion
						
						//Fetch the necessary file information from the POST request
						$language = $_POST["language"];
						$difficulty = $_POST["difficulty"];
						$roomNumber = $_POST["roomNumber"];
						
						$connection = mysqli_connect("eu-cdbr-azure-west-a.cloudapp.net", "bea59dbc864a3e", "6d5abbdc", "museum", "3306");
						
						//If a file has been uploaded and the extension is legit
						if (isset($_FILES) && $extension == $allowedExts)
						{	
							//Check for file upload errors
							if ($_FILES["file"]["error"] > 0)
							{
								echo "Error: " . $_FILES["file"]["error"] . "<br>";
							}
							else
							{
								echo "Upload: " . $_FILES["file"]["name"] . "<br>";
								echo "Type: " . $_FILES["file"]["type"] . "<br>";
								echo "Size: " . round(($_FILES["file"]["size"] / 1024)) . " kB<br>";
								
								//If the directory doesn't exist for audio of a specific language and difficulty, create it.
								if (!is_dir('audio/$language/$difficulty'))
								{
									mkdir('audio/'.$language.'/', 0777);
									mkdir('audio/'.$language.'/'.$difficulty.'/', 0777);
								}
								
								$saveLocation = "audio/$language/$difficulty/$roomNumber.$extension";
								
								//Move the uploaded file from the temp location to the directory just created.
								if (move_uploaded_file($_FILES["file"]["tmp_name"], $saveLocation))
								{
									echo "<br/><p>Stored in: $saveLocation";
								}
								
								if (mysqli_connect_errno())
								{
									echo "<p>Failed to conect to MySQL: " . mysqli_connect_error() . "</p>";
								}
								
								$databaseDirectory = "audio/$language/$difficulty/";
								
								$databaseDirectory = mysqli_real_escape_string($connection, $databaseDirectory);
								
								//Insert the file data into the database
								if (isset($language, $difficulty))
								{
									$sql = "INSERT INTO audio_file (language, difficulty, dir)
											VALUES ('$language', '$difficulty', '$databaseDirectory')";
								
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

