<?php
$TITLE = "MLTV";
$DB = "/tmp/mltv.db";

$db = new SQLite3( $DB );

function html_dashboard() {
?>
<ul id="dashboard">
	<li class="dashbtn"><a href="/">Forside</a></li>
	<li class="dashbtn"><a href="/member.php">Medlemmer</a></li>
	<li class="dashbtn"><a href="/category.php">Kategorier</a></li>
	<li class="dashbtn"><a href="/project.php">Gennemse projekter</a></li>
	<li class="dashbtn"><a href="/project.php?create">Opret projekt</a></li>
	<li class="dashbtn"><a href="/report.php">Opret rapport</a></li>

	<li class="dashbtn">
		<form method="get" action="/project.php">
			<input type="text" name="search" placeholder="Søg" />
		</form>
	</li>
</ul>
<div class="clear"></div>
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
