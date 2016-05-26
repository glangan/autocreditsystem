<!DOCTYPE html>
<html>
<head>
        <title>Units</title>
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
<table class="table table-bordered">
<tr>
        <th>Unit</th>
        <th>Institute</th>
        <th>Code</th>
        <th>Result</th>
        <th>Time</th>
        <th></th>
	<th></th>
<tr>
% for row in data:
<tr>
        <td>{{row['Unit']}}</td>
        <td>{{row['Institute']}}</td>
        <td>{{row['Code']}}</td>
        <td>{{row['Message']}}</td>
        <td>{{row['Time']}}</td>
        <td><a href='/units/{{row['_id']}}'>View</a></td>
	<td><a href='/units/delete/{{row['_id']}}' onclick="return confirm('Are you sure?')">Delete</a></td>
	
</tr>
% end
</table>
</div>
</div>
</body>
</html>
