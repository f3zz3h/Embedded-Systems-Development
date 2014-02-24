<!DOCTYPE html>
<meta charset="UTF-8">
<html>
	<head>
		<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css">
		<link rel="stylesheet" type="text/css" href="style.css">
	</head>
	<body>
		<div class="jumbotron fileUpload">
			<a class="homeLink" href="/index.html"><span class="glyphicon glyphicon-home"></span></a>
			
			<?php
				$allowedExts = "mp3";
				$temp = explode(".", $_FILES["file"]["name"]);
				$extension = end($temp);
				$language = $_POST["language"];
				$difficulty = $_POST["difficulty"];
				
				$connection = mysqli_connect("mysql.chrissewell.co.uk:3306", "root", "Lambda01", "museum");
				
				if (isset($_FILES) && strpos($_FILES["file"]["type"], "audio/") !== false && $extension == $allowedExts)
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
						
						$saveLocation = "D:\\home\\site\\files\\$language$difficulty." .$extension;
						
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
			?>	
		</div>
	</body>
</html>

