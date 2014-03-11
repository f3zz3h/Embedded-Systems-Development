<!DOCTYPE html>
<meta charset="UTF-8">
<?php session_start(); ?>
<html>
<head>
<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css" />
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
	<body>
		<div class="jumbotron login">
			<?php 
				$username = $_POST["username"];
				$password = $_POST["password"];
				
				$con = mysqli_connect("eu-cdbr-azure-west-b.cloudapp.net:3306", "bc39afe900a22c", "ab25d637", "museum");
				
				if (mysqli_connect_errno())
				{
					echo "<p>Failed to conect to MySQL: " . mysqli_connect_error() . "</p>";
				}
				
				$sql = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
				$result = mysqli_query($con, $sql);
				$row = mysqli_fetch_array($result);
				
				$con->close();
				
				if (empty($row))
				{
					$_SESSION["CanView"] = false;
					header('Location: /index.php?error=true');
				}
				else if ($username == $row[0] && $password == $row[1])
				{
					$_SESSION["CanView"] = true;
					header('Location: /portalHome.php');
				}
			?>
		</div>
	</body>
</html>