<html>
<head>
	<title>Results</title>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
	<link rel="stylesheet" href='/static/main.css'>
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
<h2>Results</h2>
<h3>Similarity Score</h3>
<p>{{float("{0:.2f}".format(data[0]))}}</p>
<h3>Recommendation</h3>
<p>{{message}}</p>
<h3>Unit Description</h3>
<p>{{desc}}</p>
<h3>Keywords</h3>
<p><ul>
	% for item in data[2]:
		<li>{{item}}</li>
	% end
</ul></p>
<h3>Learning Outcomes</h3>
<p>{{lo}}</p>
<h3>Keywords</h3>
<p><ul>
	% for item in lo_keywords:
		<li>{{item}}</li>
	% end
</ul></p>
</body>
</div>
</div>
</html>
