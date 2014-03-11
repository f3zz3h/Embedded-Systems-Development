	<!DOCTYPE html>
<meta charset="UTF-8">
<?php session_start(); ?>
<html>
<head>
<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css" />
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
	<body>
		<div class="jumbotron createCustomer">
			<?php
				if (isset($_SESSION["CanView"]))
				{
					if ($_SESSION["CanView"] == true)
					{
						echo "<a class=\"homeLink\" href=\"/portalHome.html\"><span class=\"glyphicon glyphicon-home\"></span></a>
						<h1>Museum Portal File Upload</h1>
						<br />
						<form action=\"fileUpload.php\" method=\"post\" enctype=\"multipart/form-data\">
							<div class=\"form-group\">
								<label>Language</label>
								<select class=\"form-control\" name=\"language\">";
									$lines = file('Languages.txt');

									foreach ($lines as $line_num => $line)
									{
									echo "<option>".$line."</option>";
									}
								echo "
								</select><br/>
								<label>Difficulty</label>
								<select class=\"form-control\" name=\"difficulty\">
									<option>No knowledge</option>
									<option>Primary School</option>
									<option>GCSE</option>
									<option>A-level</option>
									<option>Degree</option>
									<option>Nobel Prize winner</option>
								</select><br/>
								<input class=\"form-control\" type=\"file\" name=\"file\" id=\"file\"><br/>
								<input type=\"submit\" class=\"btn btn-primary\" />
							</div>
						</form>";
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