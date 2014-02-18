<!DOCTYPE html>
<meta charset="UTF-8">
<html>
<head>
<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css" />
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
	<body>
    <div class="jumbotron createCustomer">
	<a class="homeLink" href="/index.html"><span class="glyphicon glyphicon-home"></span></a>
        <h1>Museum handset PIN portal</h1>
        <p class="lead subHeading">Use this portal to give up your card details so they can be stored unprotected in a text file on our server.</p>
		<div class="imgHolder wobble rotateIn">
        <img src="pixel-museum.gif" style="width:220px; margin-bottom:20px;"/>
		</div>

	  <form action="customer.php" method="post">
	  <div class="form-group">
			<label>Name:</label><input class="form-control" type="text" name="name" required="required"/><br/>
			<label>Address:</label><input class="form-control" type="text" name="address" required="required"/><br/>
			<label>Mobile #:</label><input class="form-control" type="text" name="mobileNumber" required="required"/><br/>
			<label>Language:</label>
			<select class="form-control" name="language">
				<?php
					$lines = file('Languages.txt');
					
					foreach ($lines as $line_num => $line)
					{
						echo "<option>".$line."</option>";
					}
				?>
			</select><br/>
			<label>Competence level:</label>
			<select class="form-control" name="knowledge">
				<option>No knowledge</option>
				<option>Primary School</option>
				<option>GCSE</option>
				<option>A-level</option>
				<option>Degree</option>
				<option>Nobel Prize winner</option>
			</select><br/>
			<label>Payment card number:</label><input class="form-control" id="CardNumber" name="cardNumber" type="text" /><br/>
			<div class="clear"/>
			<input type="submit" value="Save" class="btn btn-primary" id="btn"/>
		</form>
		</div>
	</div>
  </body>
</html>