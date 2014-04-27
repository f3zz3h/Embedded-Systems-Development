<!DOCTYPE html>
<meta charset="UTF-8" http-equiv="refresh" content="4;url=/manageFiles.php">
<?php session_start(); ?>
<html>
<head>
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

					$con = mysqli_connect("eu-cdbr-azure-west-b.cloudapp.net", "bc39afe900a22c", "ab25d637", "museum", "3306");
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

