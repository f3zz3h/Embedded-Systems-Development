<!DOCTYPE html>
<meta charset="UTF-8">
<?php
	//loginUser.php - Handles user login and redirects to the relevant page.
	session_start(); 


	$username = $_POST["username"];
	$password = $_POST["password"];

	$con = mysqli_connect("eu-cdbr-azure-west-b.cloudapp.net", "bc39afe900a22c", "ab25d637", "museum", "3306");

	if (mysqli_connect_errno())
	{
		echo "<p>Failed to conect to MySQL: " . mysqli_connect_error() . "</p>";
	}

	//Build the SQL query
	$sql = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
	$result = mysqli_query($con, $sql);
	$row = mysqli_fetch_array($result);

	$con->close();

	if (empty($row))
	{
		//No user credentials matched, return to index.php with error query string parameter
		$_SESSION["CanView"] = false;
		header('Location: /index.php?error=true');
	}
	else if ($username == $row[0] && $password == $row[1])
	{
		//User credentials matched, set session variable and redirect to portalHome.php
		$_SESSION["CanView"] = true;
		header('Location: /portalHome.php');
	}
			
?>