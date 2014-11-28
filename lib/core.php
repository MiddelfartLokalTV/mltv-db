<?php
$TITLE = "MLTV";
$DB = "/tmp/mltv.db";

$db = new SQLite3( $DB );

function html_header($TITLE) {
?>
<meta charset="utf-8">
<link rel="stylesheet" href="css/style.css" />
<link rel="icon" type="image/png" href="logo_traced.png" />
<title><?php echo $TITLE ?></title>
<?php
}

function html_dashboard() {
?>
<ul id="dashboard">
	<li class="dashbtn"><a href=".">Forside</a></li>
	<li class="dashbtn"><a href="member.php">Medlemmer</a></li>
	<li class="dashbtn"><a href="category.php">Kategorier</a></li>
	<li class="dashbtn"><a href="project.php">Gennemse Projekter</a></li>
	<li class="dashbtn"><a href="project.php?edit">Opret Projekt</a></li>
	<li class="dashbtn"><a href="report.php">Opret Rapport</a></li>

	<li class="dashbtn">
		<form method="get" action="project.php">
			<input type="text" name="search" placeholder="Søg" />
		</form>
	</li>
</ul>
<div class="clear"></div>
<?php
}

function html_logo () {
?>
<div id="header">
	<a href="."><img id="logo" src="logo.gif" /></a>
</div>
<br/>
<?php
}

function html_sidebar() {
	global $db;
?>
<div id="sidebar">
	<b>Nyligt oprettede projekter:</b>
	<table>
<?php
	$query = $db->query( "SELECT id,title FROM projects ORDER BY id DESC LIMIT 15" );
	while( $row = $query->fetchArray() ) {
?>
	<tr>
		<td><a href="project.php?id=<?php echo $row["id"];?>"><?php echo $row["id"];?></a></td>
		<td><a href="project.php?id=<?php echo $row["id"];?>"><?php echo $row["title"];?></a></td>
	</tr>
<?php
	}
?>
	</table>
</div>
<?php
}

function html_footer() {
?>
<div id="footer">
	<p>
System og design af <a href="http://necrophcodr.me">Steffen Rytter Postas</a>
Copyright &copy; 2014 <a href="http://www.middelfart.tv">Middelfart Lokal TV</a>
	</p>
</div>
<?php
}
?>
