<!DOCTYPE html>
<meta charset="UTF-8">
<html>
<head>
<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css" />
<link rel="stylesheet" type="text/css" href="bootstrap/css/jumbotron.css" />
</head>
	<body>
    <div class="container">
      <div class="jumbotron">
        <h1>Museum handset PIN portal</h1>
        <p class="lead subHeading">Use this portal to give up your card details so they can be stored unprotected in a text file on our server.</p>
		<div class="imgHolder wobble rotateIn">
        <img src="pixel-museum.gif" style="width:220px; margin-bottom:20px;"/>
		</div>
      </div>

      <div class="row marketing">
		<div class="inputBoxes">
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
				<input type="submit" value="Save" class="btn" id="btn"/>
			</form>
		</div>
      </div>
    </div>
  </body>
</html>