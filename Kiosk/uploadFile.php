<!DOCTYPE html>
<meta charset="UTF-8">
<?php session_start(); ?>
<html>
<head>
<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css" />
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
	<body>
		<div class="jumbotron narrow">
			<?php
				if (isset($_SESSION["CanView"]))
				{
					if ($_SESSION["CanView"] == true)
					{
						echo "<a class=\"homeLink\" href=\"/portalHome.php\"><span class=\"glyphicon glyphicon-home\"></span></a>
						<h1>Museum Portal File Upload</h1>
						<br />
						<form action=\"fileUpload.php\" method=\"post\" enctype=\"multipart/form-data\">
							<div class=\"form-group\">
								<label>Language</label>
								<select class=\"form-control\" name=\"language\" required=\"required\">";
									//Extract each line from the languages file
									$lines = file('Languages.txt');

									//Iterate through the lines variable and create a select option for each language.
									foreach ($lines as $line_num => $line)
									{
									echo "<option>".$line."</option>";
									}
								echo "
								</select><br/>
								<label>Difficulty</label>
								<select class=\"form-control\" name=\"difficulty\" required=\"required\">
									<option value=\"noknowledge\">No knowledge</option>
									<option value=\"primaryschool\">Primary School</option>
									<option>GCSE</option>
									<option value=\"alevel\">A-level</option>
									<option>Degree</option>
									<option value=\"nobelprize\">Nobel Prize winner</option>
								</select><br/>
								<label>File</label>
								<input class=\"form-control\" type=\"file\" name=\"file\" id=\"file\"><br/>
								<label>Room number</label>
								<input class=\"form-control\" type=\"textbox\" name=\"roomNumber\" required=\"required\"/>
								</br>
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