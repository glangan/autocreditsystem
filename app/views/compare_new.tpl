<!DOCTYPE html>
<html>
<head>
	<title>Auto Unit Credit Assignment System</title>
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
<h3>Compare New Units</h3>
<form action = "/compare_new" method = "POST">
<div class="form-group">
<label for="unit">Select a unit: </label>
<select id="unitList" name="utasunits">
	<option value = "KIT101">KIT101: Programming Fundamentals</option>
	<option value = "KIT205">KIT205: Data Structures and Algorithms</option>
</select>
</div>
<div class="form-group">
<label for="uni">Institute: </label>
<input type="text" name="uni">
</div>
<div class="form-group">
<label for="code">Unit Code: </label>
<input type="text" name="code">
</div>
<label for"level">Level: </label>
<select id="level" name="level">
	<option value="1">Level 1 - Introductory</option>
	<option value="2">Level 2 - Intermediate</option>
</select>
<div class="form-group">
<label for="description">Unit Description: </label>
<textarea name="description" class="form-control" rows="3"></textarea>
</div>
<div class="form-group">
<label for"lo">Learning Outcomes: </label>
<textarea name="lo" class="form-control" rows="3"></textarea>
</div>
<input type="submit" name="submit" value="Submit" class="btn btn-default"	>
</form>
</div>
</div>
</body>
</html>
