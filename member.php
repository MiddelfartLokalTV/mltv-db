<?php
include_once( "lib/core.php" );
if( isset( $_POST["name"] ) ) {
		$id = isset( $_POST["id"] ) ? $_POST["id"] : "";
		if( strcmp($id,"") === 0 ) {
			// no id given, INSERT
			$name		= isset( $_POST["name"] ) ? $_POST["name"] : "";
			$phone	= isset( $_POST["phone"] ) ? $_POST["phone"] : "";
			$email	= isset( $_POST["email"] ) ? $_POST["email"] : "";
			$db->exec( "INSERT INTO members VALUES( NULL, '".$name."','".$phone."','".$email."')" );
			$id = $db->querySingle( "SELECT MAX(id) FROM members" );
			header( "Location: member.php?id=" . $id["id"] );
		} else {
			// id received, UPDATE
			$stmt = $db->prepare( "UPDATE members SET name = :name, phone = :phone, email = :email WHERE id == ". $id );
			$stmt->bindValue( ":name", $_POST["name"], SQLITE3_TEXT );
			$stmt->bindValue( ":phone", $_POST["phone"], SQLITE3_TEXT );
			$stmt->bindValue( ":email", $_POST["email"], SQLITE3_TEXT );
			$stmt->execute();
			header( "Location: member.php?id=" . $id );
		}
}
?>

<!doctype html>
<html>
	<head>
		<?php html_header($TITLE . " - Medlemmer"); ?>
	</head>
	<body>
		<div id="wrapper">
			<?php html_dashboard(); ?>
			<div id="content">
				<?php html_logo(); ?>
<?php if( isset( $_GET["id"] ) and !isset( $_GET["edit"] ) ) {
			$member = isset( $_GET["id"] ) ? $db->querySingle("SELECT * FROM members WHERE id == " . $_GET["id"], true ) : "";
			// Ensure that these variables are NOT empty, and set their correct values
			// if they exist.
			$id				= isset( $member["id"] ) ? $member["id"] : "";
			$name			= isset( $member["name"] ) ? $member["name"] : "";
			$phone		= isset( $member["phone"] ) ? $member["phone"] : "";
			$email		= isset( $member["email"] ) ? $member["email"] : "";

?>
			<div id="sidebar">
				<a href="member.php?id=<? echo $id?>&amp;edit">Redigér</a>
			</div>

			<h2><?echo $name?></h2>
			<b>Mobil</b>: <? echo $phone?><br/>
			<b>E-Mail</b>: <?echo $email?><br/>
			<p><? echo $name?> har produceret følgende:</p>
			<table>
				<thead>
					<tr>
						<th>Projekt Nr.</th>
						<th>Projekt Titel</th>
					</tr>
				</thead>
				<tbody>

<?php } elseif( isset( $_GET["edit"] ) ) { 
			$member = isset( $_GET["id"] ) ? $db->querySingle("SELECT * FROM members WHERE id == " . $_GET["id"], true ) : "";
			// Ensure that these variables are NOT empty, and set their correct values
			// if they exist.
			$id				= isset( $member["id"] ) ? $member["id"] : "";
			$name			= isset( $member["name"] ) ? $member["name"] : "";
			$phone		= isset( $member["phone"] ) ? $member["phone"] : "";
			$email		= isset( $member["email"] ) ? $member["email"] : "";

			$projecs	= isset( $member["id"] ) ? $db->querySingle("SELECT id FROM projects WHERE producer == '" . $member["id"] . "'" ) : [];
?>
			<div id="sidebar">
				<a href="#" onClick="memberSave();">Gem</a>
			</div>
			<form action="member.php" method="post">
				<input type="hidden" name="id" value="<? echo $id ?>"/>
				<label><b>Navn</b>:</label>
					<input type="text" name="name" value="<? echo $name ?>"/>
				<label><b>Telefon</b>:</label>
					<input type="text" name="phone" value="<? echo $phone?>"/>
				<label><b>E-Mail</b>:</label>
					<input type="email" name="email" value="<? echo $email ?>" />
				<input type="submit" name="submit" style="display:none;"/>
			</form>
			<?php
			?>
				</tbody>
			</table>
			<?php } else { ?>
				<div id="sidebar">
					<a href="member.php?edit">Tilføj Medlem</a>
				</div>

			<table>
				<thead>
					<tr>
						<th><b>Navn</b></th>
						<th><b>Telefon</b></th>
						<th><b>E-Mail</b></th>
						<th><b>Antal producerede projekter</b></th>
					</tr>
				</thead>
			<?php
				$members = $db->query( "SELECT * FROM members" );
				while( $member = $members->fetchArray() ) {
					$proj_count = $db->querySingle( "SELECT count(id) FROM projects WHERE producer == " . $member["id"] );
?>
				<tr>
					<td><a href="member.php?id=<?php echo $member["id"]?>"><?php echo $member["name"]?></a></td>
					<td><? echo $member["phone"] ?></td>
					<td><a href="mailto:<?php echo $member["email"]?>"><?php echo $member["email"]?></a></td>
					<td><a href="member.php?id=<?php echo $member["id"]?>"><?php echo $proj_count?></a></td>
				</tr>
			<?php } } ?>
				</tbody>
				</table>
			</div>
		</div>
		<?php html_footer(); ?>
		<script>
			function memberSave() {
				document.getElementsByTagName("form")[1].submit.click();
			}		
		</script>
	</body>
</html>
