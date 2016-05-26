<!DOCTYPE html>
<head>
	<title>Auto Unit credit Assignment System :: UTAS</title>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
	<link rel="stylesheet" href='static/main.css'>
</head>
<body>
	<div class="container">
	<div class="row">
	<h1>Auto Unit Credit Assignment System</h1>
	<nav>
		<a href = "/">Home</a>
		<a href = "/compare_new">Compare New Unit</a>
		<a href = "/units">List Units</a>
		<a href = "/history">History</a>
	</nav>
	<h2>About</h2>
	<p>Automated Unit Credit Assignment System is based on the Wikipedia Link Model for finding similarity between concepts. This system uses unit description or topics covered in a unit to find similarity between two units. This system can be used to find similar units to KIT101 (Programming Fundamentals) and KIT205 (Data Structure and Algorithms) taught at the University of Tasmania.
	<h2>Usage</h2>
	<p><ul>
	<li>Only the unit description is used to find similarity between units.</li>
	<li>The similarity score in the range of 0-1 will be given in the output, along with the keywords from the unit description provided.</li>
	<li>If learning outcomes is also provided, the system will find keywords from it</li>
	<li>If the name of the institute and unit code or name is provided, the unit results will be saved for future use.</li>
	</ul></p>
	</div>
	</div>
</body>
</html>
