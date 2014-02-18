<!DOCTYPE html>
<meta charset="UTF-8">
<html>
<head>
<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css" />
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
	<body>
    <div class="jumbotron updateCustomer">
	<a class="homeLink" href="/index.html"><span class="glyphicon glyphicon-home"></span></a>
        <h1>Museum portal update customer</h1>
		<br/>
	<?php
		$id = $_GET['id'];
		$encryptionMethod = 'aes128';
		$password = 'ESD';

		$con=mysqli_connect("mysql.chrissewell.co.uk:3306","root","Lambda01","museum");
		// Check connection
		if (mysqli_connect_errno())
		{
		echo "Failed to connect to MySQL: " . mysqli_connect_error();
		}

		$result = mysqli_query($con,"SELECT * FROM customer WHERE id = $id");

		$customer = mysqli_fetch_array($result);
		
		$cardNumber = openssl_decrypt($customer[6], $encryptionMethod, $password);
		
		echo "<form action=\"customer.php\" method=\"post\">
		<input type=\"hidden\" name=\"id\" value=\"$customer[0]\"/>
		<div class=\"form-group\">
			<label>Name:</label><input class=\"form-control\" type=\"text\" name=\"name\" required=\"required\" value=\"$customer[1]\"/><br/>
			<label>Address:</label><input class=\"form-control\" type=\"text\" name=\"address\" required=\"required\" value=\"$customer[3]\"/><br/>
			<label>Mobile #:</label><input class=\"form-control\" type=\"text\" name=\"mobileNumber\" required=\"required\" value=\"$customer[2]\"/><br/>
			<label>Language:</label>
			<select class=\"form-control\" name=\"language\">";
					$lines = file('Languages.txt');
					
					foreach ($lines as $line_num => $line)
					{
						echo "<option>".$line."</option>";
					}
			echo "</select><br/>
			<label>Competence level:</label>
			<select class=\"form-control\" name=\"knowledge\">
				<option>No knowledge</option>
				<option>Primary School</option>
				<option>GCSE</option>
				<option>A-level</option>
				<option>Degree</option>
				<option>Nobel Prize winner</option>
			</select><br/>
			<label>Payment card number:</label><input class=\"form-control\" id=\"CardNumber\" name=\"cardNumber\" type=\"text\" value=\"$cardNumber\" /><br/>
			<div class=\"clear\"/>
			<input type=\"submit\" value=\"Save\" class=\"btn btn-primary\" id=\"btn\"/>
		</form>";
		
		mysqli_close($con);
	?>
	</div>
  </body>
</html>