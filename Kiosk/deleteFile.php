<!DOCTYPE html>
<meta charset="UTF-8" http-equiv="refresh" content="4;url=/manageFiles.php">
<html>
<head>
	<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css">
	<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
	<div class="jumbotron deleteFile">
		<?php
			$id;
		
			if (!isset($_GET['id']))
			{
				echo "<p><b>Error: No file ID found.. Please wait.</b></p>";
				echo "<br/>";
				echo "<span class=\"glyphicon glyphicon-refresh\"</span>";
				exit;
			}
			else
			{
				$id = $_GET['id'];
			}
			
			if (!isset($_GET['loc']))
			{
				echo "<p><b>Error: No file location found.. Please wait.</b></p>";
				echo "<br/>";
				echo "<span class=\"glyphicon glyphicon-refresh\"</span>";
				exit;
			}
			else
			{
				$loc = $_GET['loc'];
			}

			$con=mysqli_connect("mysql.chrissewell.co.uk:3306","root","Lambda01","museum");
			if ($con->connect_error)
			
			{
				die('Connect Error (' . $con->connect_errno . ') ' . $con->connect_error);
			}

			$sql = "DELETE FROM audio_file WHERE id = $id";
			if (!$result = $con->prepare($sql))
			{
				die('Query failed: (' . $con->errno . ') ' . $con->error);
			}

			if (!$result->execute())
			{
				die('Execute failed: (' . $result->errno . ') ' . $result->error);
			}

			if (unlink($loc))
			{
				echo "<p><b>File deleted.. Please wait.</b></p>";
				echo "<br/>";
				echo "<span class=\"glyphicon glyphicon-refresh\"</span>";
				exit;
			}
			else
			{
				echo "<p><b>Error deleting file.. Please wait.</b></p>";
				echo "<br/>";
				echo "<span class=\"glyphicon glyphicon-refresh\"</span>";
				exit;
			}
			
			$result->close();
			$con->close();
		?>
	</div>
</body>
</html>

