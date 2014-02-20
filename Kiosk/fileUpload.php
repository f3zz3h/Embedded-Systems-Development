<!DOCTYPE html>
<meta charset="UTF-8">
<html>
	<head>
		<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css">
		<link rel="stylesheet" type="text/css" href="style.css">
	</head>
	<body>
		<div class="jumbotron customer">
			<a class="homeLink" href="/index.html"><span class="glyphicon glyphicon-home"></span></a>
			
			<?php
				$allowedExts = "mp3";
				$temp = explode(".", $_FILES["file"]["name"]);
				$extension = end($temp);
				
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
						echo "Size: " . ($_FILES["file"]["size"] / 1024) . " kB<br>";
						
						$saveLocation = "/site/files/" . $_FILES["file"]["name"];
						
						if (move_uploaded_file($_FILES["file"]["tmp_name"], $saveLocation))
						{
							echo "<p>Stored in: " . "/site/files" . $_FILES["file"]["name"];
						}
					}
				}
				else
				{
					echo "<p> umm no. </p>";
				}
			?>	
		</div>
	</body>
</html>

