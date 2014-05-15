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
				//Create the home page link
				echo "<a class=\"homeLink\" href=\"/portalHome.php\"><span class=\"glyphicon glyphicon-home\"></span></a>
				<h1>Museum portal update customer</h1>
				<br/>";
			
				//Get the ID of the customer from the query string.
				$id = $_GET['id'];
				
				//Set the encryption type and password for card numbers
				$encryptionMethod = 'aes128';
				$password = 'ESD';

				//Create the MySQL connection object
				$con = mysqli_connect("eu-cdbr-azure-west-a.cloudapp.net", "bea59dbc864a3e", "6d5abbdc", "museum", "3306");
				
				// Check connection success
				if (mysqli_connect_errno())
				{
				echo "Failed to connect to MySQL: " . mysqli_connect_error();
				}

				//Execute the query and return the resultant MySQL object into the result variable.
				$result = mysqli_query($con,"SELECT * FROM customer WHERE id = $id");

				//Get the resultant array of data from the result variable
				$customer = mysqli_fetch_array($result);
				
				//Decrypt card number for dispaly purposes
				$cardNumber = openssl_decrypt($customer[6], $encryptionMethod, $password);
				
				//Render page HTML
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