<!DOCTYPE html>
<meta charset="UTF-8" http-equiv="refresh" content="4;url=/manageUsers.php">
<?php session_start(); ?>
<html>
<head>
	<!-- deleteCustomer.php - deletes a customers details from the database-->
	<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css">
	<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
	<div class="jumbotron narrow">
		<?php
			//Check access
			if (isset($_SESSION["CanView"]))
			{
				if ($_SESSION["CanView"] == true)
				{
					$id;
				
					//If no ID was password with the query string we can't delete anyone
					if (!isset($_GET['id']))
					{
						echo 'No ID was given...';
						exit;
					}
					else
					{
						$id = $_GET['id'];
					}

					$con = mysqli_connect("eu-cdbr-azure-west-b.cloudapp.net", "bc39afe900a22c", "ab25d637", "museum", "3306");
					
					if ($con->connect_error)
					{
						die('Connect Error (' . $con->connect_errno . ') ' . $con->connect_error);
					}

					//Build deletion SQL
					$sql = "DELETE FROM customer WHERE id = $id";
					
					//If the result failed, die.
					if (!$result = $con->prepare($sql))
					{
						die('Query failed: (' . $con->errno . ') ' . $con->error);
					}

					if (!$result->execute())
					{
						die('Execute failed: (' . $result->errno . ') ' . $result->error);
					}

					//Otherwise, display confirmation message and redirect back to the manage users page.
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

