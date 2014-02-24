<!DOCTYPE html>
<meta charset="UTF-8">
<html>
<head>
<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css" />
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
	<body>
    <div class="jumbotron manageFiles">
	<a class="homeLink" href="/index.html"><span class="glyphicon glyphicon-home"></span></a>
        <h1>Museum portal manage files</h1>
		<br/>
	<?php
		$con=mysqli_connect("mysql.chrissewell.co.uk:3306","root","Lambda01","museum");
		// Check connection
		if (mysqli_connect_errno())
		{
		echo "Failed to connect to MySQL: " . mysqli_connect_error();
		}

		$result = mysqli_query($con, "SELECT * FROM audio_file");

		echo "<table class=\"table table-striped\">";
		echo "<thead><th>Language</th><th>Difficulty</th><th>Location</th><th>Delete</th></thead>";
		echo "<tbody>";
		
		while($row = mysqli_fetch_array($result))
		{
			echo "<tr><td>$row[1]</td><td>$row[2]</td><td>$row[3]</td><td><a href=\"/deleteFile.php?id=$row[0]&loc=$row[3]\"><span class=\"glyphicon glyphicon-remove\"></span></a></td></tr>";
		}

		echo "</tbody></table>";
		
		mysqli_close($con);
	?>
	</div>
  </body>
</html>