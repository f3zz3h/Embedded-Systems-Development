<!DOCTYPE html>
<meta charset="UTF-8">
<html>
<head>
<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css" />
</head>
	<body>
			<h1>Museum handset PIN portal</h1>
			<form action="customer.php" method="post">
				<label>Name:</label><input type="text" name="name" required="required"/>
				<label>Address:</label><input type="text" name="address" required="required"/>
				<label>Mobile #:</label><input type="text" name="mobileNumber" required="required"/>
				<label>Language:</label>
				<select name="language">
					<?php
						$lines = file('Languages.txt');
						
						foreach ($lines as $line_num => $line)
						{
							echo "<option>".$line."</option>";
						}
					?>
				</select>
				<label>Competence level:</label>
				<select name="knowledge">
					<option>No knowledge</option>
					<option>Primary School</option>
					<option>GCSE</option>
					<option>A-level</option>
					<option>Degree</option>
					<option>Nobel Prize winner</option>
				</select>
				<label>Payment card number:</label><input id="CardNumber" name="cardNumber" type="text" />
				<div class="clear"/>
				<input type="submit" value="Save" id="btn"/>
			</form>
	</body>
</html>