<!DOCTYPE html>
<meta charset="UTF-8">
<?php session_start(); ?>
<html>
<head>
<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css" />
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
	<body>
		<div class="jumbotron index">
			<h1>Museum Portal Index</h1>
			
		<form method="post" action="loginUser.php">
			<div class="form-group">
				<label>Username:</label><input class="form-control" type="text" name="username"/>
				<label>Password:</label><input class="form-control" type="password" name="password"/>
				<?php
					if (isset($_GET["error"]))
					{
						$error = $_GET["error"];
						
						if ($error == true)
						{
								echo "<label style=\"color:red;\">Incorrect password.</label>";
						}
					}
				?>
				</br>
				<input type="submit" class="btn btn-primary" value="Login" />
			</div>
		</form>
	</body>
</html>