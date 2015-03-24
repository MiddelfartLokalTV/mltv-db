<?php
global $db;
?>
<div id="sidebar">
	<b>Nyligt oprettede projekter:</b>
	<table>
<?php
$query = $db->query( "SELECT id,title FROM projects ORDER BY id DESC LIMIT 15" );
	if( $query != false ) {
		while( $row = $query->fetchArray() ) {
?>
	<tr>
		<td><a href="project.php?id=<?php echo $row["id"];?>"><?php echo $row["id"];?></a></td>
		<td><a href="project.php?id=<?php echo $row["id"];?>"><?php echo $row["title"];?></a></td>
	</tr>
<?php
	} }
?>
	</table>
</div>

