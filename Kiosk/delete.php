<!DOCTYPE html>
<meta charset="UTF-8" http-equiv="refresh" content="4;url=/manageUsers.php">
<html>
<head>
	<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css">
	<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
	<div class="jumbotron delete">
		<?php
			$id;
		
			if (!isset($_GET['id']))
			{
				echo 'No ID was given...';
				exit;
			}
			else
			{
				$id = $_GET['id'];
			}

			$con=mysqli_connect("mysql.chrissewell.co.uk:3306","root","Lambda01","museum");
			if ($con->connect_error)
			
			{
				die('Connect Error (' . $con->connect_errno . ') ' . $con->connect_error);
			}

			$sql = "DELETE FROM customer WHERE id = $id";
			if (!$result = $con->prepare($sql))
			{
				die('Query failed: (' . $con->errno . ') ' . $con->error);
			}

			if (!$result->execute())
			{
				die('Execute failed: (' . $result->errno . ') ' . $result->error);
			}

			if ($result->affected_rows > 0)
			{
				echo "<b>Customer Deleted.. Please wait.</b>";
				echo "<br/>";
				echo "<span class=\"glyphicon glyphicon-refresh\"</span>";
			}
			else
			{
				echo "Couldn't delete the ID.";
			}
			
			$result->close();
			$con->close();
		?>
	</div>
</body>
</html>

