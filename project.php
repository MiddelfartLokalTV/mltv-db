<?php
include_once( "lib/core.php" );

if( isset( $_POST["title"] ) ) {
	$proj_title			= isset( $_POST["title"] ) ? $_POST["title"] : "";
	$proj_desc			= isset( $_POST["desc"] ) ? $_POST["desc"] : "";
	$proj_producer	= isset( $_POST["producer"] ) ? $_POST["producer"] : "";
	$proj_editor		= isset( $_POST["editor"] ) ? $_POST["editor"] : "";
	$proj_cat				= isset( $_POST["category"] ) ? $_POST["category"] : "";
	$proj_music			= isset( $_POST["music"] ) ? $_POST["music"] : "";
	$proj_created		= isset( $_POST["created"] ) ? $_POST["created"] : "";
	$proj_exp_done	= isset( $_POST["expected_done"] ) ? $_POST["expected_done"] : "";
	$proj_exp_len		= isset( $_POST["expected_length"] ) ? $_POST["expected_length"] : "";
	$proj_real_len	= isset( $_POST["real_length"] ) ? $_POST["real_length"] : "";
	$proj_timespan	= isset( $_POST["timespan"] ) ? $_POST["timespan"] : "";
	$proj_release		= isset( $_POST["release"] ) ? $_POST["release"] : "";
	$proj_rel_type	= isset( $_POST["release_type"] ) ? $_POST["release_type"] : "";
	$proj_part			= isset( $_POST["participants"] ) ? $_POST["participants"] : "";

	$SQL = "INSERT INTO projects VALUES( NULL, :title, :desc, :producer, :editor, :category, :music, :created, :expected_done, :expected_length, :real_length, :timespan, :release, :release_type, :participants )";
	if( isset( $_POST["id"] ) ) {
		// We're updating the project
		$proj						= $_POST["id"];
		$SQL = "UPDATE projects SET title = :title, desc = :desc, producer = :producer, editor = :editor, category = :category, music = :music, created = :created, expected_done = :expected_done, expected_length = :expected_length, real_length = :real_length, timespan = :timespan, release = :release, release_type = :release_type, participants = :participants WHERE id = ".$proj;
	}
	header( "Location: project.php?id=".$proj );
	$stmt = $db->prepare( $SQL );
	$stmt->bindValue( ":title", $proj_title, SQLITE3_TEXT );
	$stmt->bindValue( ":desc", $proj_desc, SQLITE3_TEXT );
	$stmt->bindValue( ":producer", $proj_producer, SQLITE3_INTEGER );
	$stmt->bindValue( ":editor", $proj_editor, SQLITE3_INTEGER );
	$stmt->bindValue( ":category", $proj_cat, SQLITE3_INTEGER );
	$stmt->bindValue( ":music", $proj_music, SQLITE3_TEXT );
	$stmt->bindValue( ":created", $proj_created, SQLITE3_TEXT );
	$stmt->bindValue( ":expected_done", $proj_exp_done, SQLITE3_TEXT );
	$stmt->bindValue( ":expected_length", $proj_exp_len, SQLITE3_TEXT );
	$stmt->bindValue( ":real_length", $proj_real_len, SQLITE3_TEXT );
	$stmt->bindValue( ":timespan", $proj_timespan, SQLITE3_TEXT );
	$stmt->bindValue( ":release", $proj_release, SQLITE3_TEXT );
	$stmt->bindValue( ":release_type", $proj_rel_type, SQLITE3_TEXT );
	$stmt->bindValue( ":participants", $proj_part, SQLITE3_TEXT );
	$stmt->execute();
	$location = "";
	if( isset( $_POST["id"] ) ) {
		$location = "Location: project.php?id=".$_POST["id"];
	} else {
		$id = $db->querySingle( "SELECT MAX(id) FROM projects", true );
		$location = "Location: project.php?id=".$id["id"];
	}
	header( $location );
	exit(0);
}
?>

<!doctype html>
<html>
	<head>
		<?php html_header($TITLE . " - Projekt"); ?>
	</head>
	<body>
		<div id="wrapper">
			<?php html_dashboard(); ?>
			<div id="content">
				<?php html_logo(); ?>
				<?php if( isset( $_GET["id"] ) and !isset( $_GET["edit"] ) ) {
					if( $_GET["id"] != 0 && $_GET["id"] != "" ) {	
						$project				= $db->query( "SELECT * FROM projects WHERE id == " . $_GET["id"] )->fetchArray();
						$proj						= $project["id"];
						$proj_title			= $project["title"];
						$proj_desc			= $project["desc"];
						$proj_producer	= $project["producer"];
						$proj_editor		= $project["editor"];
						$proj_cat				= $project["category"];
						$proj_music			= $project["music"];
						$proj_created		= $project["created"];
						$proj_exp_done	= $project["expected_done"];
						$proj_exp_len		= $project["expected_length"];
						$proj_real_len	= $project["real_length"];
						$proj_timespan	= $project["timespan"];
						$proj_release		= $project["release"];
						$proj_rel_type	= $project["release_type"];
						$proj_part			= $project["participants"];
					?>
					<div id="sidebar">
						<a href="project.php?edit&amp;id=<?php echo $proj?>">Redigér</a>
					</div>
					<h3><? echo $proj ?>&nbsp; - &nbsp; <? echo $proj_title ?></h3>
					<table id="project-view">
						<tr>
							<td><b>Producer</b>: <? echo $proj_producer ?></td>
							<td><b>Oprettet</b>: <? echo $proj_created ?></td>
						</tr>
					</table>
					<?php						
					}
				} elseif( isset( $_GET["edit"] ) ) { 
					$project = [];
					if( isset( $_GET["id"] ) ) { 
						$project				= $db->query( "SELECT * FROM projects WHERE id == " . $_GET["id"] )->fetchArray();
					}
					$proj						= isset( $project["id"] ) ? $project["id"] : "";
					$proj_title			= isset( $project["title"] ) ? $project["title"] : "";
					$proj_desc			= isset( $project["desc"] ) ? $project["desc"] : "";
					$proj_producer	= isset( $project["producer"] ) ? $project["producer"] : "";
					$proj_editor		= isset( $project["editor"] ) ? $project["editor"] : "";
					$proj_cat				= isset( $project["category"] ) ? $project["category"] : "";
					$proj_music			= isset( $project["music"] ) ? $project["music"] : "";
					$proj_created		= isset( $project["created"] ) ? $project["created"] : "";
					$proj_exp_done	= isset( $project["expected_done"] ) ? $project["expected_done"] : "";
					$proj_exp_len		= isset( $project["expected_length"] ) ? $project["expected_length"] : "";
					$proj_real_len	= isset( $project["real_length"] ) ? $project["real_length"] : "";
					$proj_timespan	= isset( $project["timespan"] ) ? $project["timespan"] : "";
					$proj_release		= isset( $project["release"] ) ? $project["release"] : "";
					$proj_rel_type	= isset( $project["release_type"] ) ? $project["release_type"] : "";
					$proj_part			= isset( $project["participants"] ) ? $project["participants"] : "";
				?>
				<div id="sidebar">
					<a href="#" onClick="projectSave();">Gem</a>
				</div>
				<form method="post" action="project.php">
					<div class="form_project">
						<label>Projekt Navn:</label>
						<input type="text" name="title" value="<? echo $proj_title ?>"/>
						<label>Projekt Nummer:</label>
							<? if( isset($proj) ) { ?>
							<input type="text" name="id" readonly="readonly" value="<? echo $proj; ?>"/>
							<? } else { ?>
							<input type="text" name="id" placeholder="nyt" disabled="disabled" />
							<? } ?>
						<label>Producer:</label>
							<select name="producer">
								<? $members = $db->query( "SELECT id,name FROM members" );
								while( $member = $members->fetchArray() ) {
								if( $proj_producer === $member["id"] ) { ?>
								<option selected="selected" value="<? echo $member["id"] ?>"><? echo $member["name"] ?></option>
								<? } else { ?>
								<option value="<? echo $member["id"] ?>"><? echo $member["name"] ?></option>
								<? } } ?>
							</select>
						<label>Oprettet:</label>
						<input type="date" name="created" value="<? echo $proj_created ?>" />
						<label>Redigering:</label>
							<select name="editor">
								<? $members = $db->query( "SELECT id,name FROM members" );
								while( $member = $members->fetchArray() ) {
								if( $proj_producer === $member["id"] ) { ?>
								<option selected="selected" value="<? echo $member["id"] ?>"><? echo $member["name"] ?></option>
								<? } else { ?>
								<option value="<? echo $member["id"] ?>"><? echo $member["name"] ?></option>
								<? } } ?>
							</select>
						<label>Kategori</label>
							<select name="category">
								<? $categories = $db->query( "SELECT * FROM categories" );
					while( $category = $categories->fetchArray() ) { 
						if( $category["id"] === $proj_cat ) { ?>
							<option selected="selected" value="<? echo $category["id"] ?>"><? echo $category["name"] ?></option>
							<? } else { ?>									
							<option value="<? echo $category["id"] ?>"><? echo $category["name"] ?></option>
								<? } } ?>
							</select>
						<label>Beskrivelse til YouTube:</label>
						<textarea cols="80" rows="12" name="desc"><? echo htmlentities($proj_desc) ?></textarea>
						<label>Deltagende:</label>
						<textarea name="participants"><? echo htmlentities($proj_part) ?></textarea>
						<label>Musik:</label>
						<input type="text" name="music" value="<? echo $proj_music ?>"/>
						<label>Forventet Færdig:</label>
						<input type="date" name="exp_done" value="<? echo $proj_exp_done ?>"/>
						<label>Forventet Længde: (TT:MM:SS)</label>
						<input type="text" name="exp_length" value="<? echo $proj_exp_len ?>"/>
						<label>Udgivet:</label>
						<input type="date" name="release" value="<? echo $proj_release ?>"/>
						<label>Aktuel Længde: (TT:MM:SS)</label>
						<input type="text" name="real_length" value="<? echo $proj_real_len ?>"/>
							<input type="submit" name="submit" style="display:none;"/>
						</div>
				</form>
				<? } else {
				$projects		= $db->query( "SELECT id, title FROM projects ORDER BY id DESC LIMIT 20" );
				$categories	= $db->query( "SELECT * FROM categories" );
?>
				<div id="sidebar">
					<? while( $category = $categories->fetchArray() ) { ?>
						<a href="project.php?cat=<? echo $category["id"] ?>"><? echo $category["name"] ?></a><br/>
					<?	}	?>
				</div>
				<table>
					<thead>
						<tr>
							<th>Projekt Nr.</th>
							<th>Projekt Titel</th>
						</tr>
					</thead>
					<tbody>
<? while( $project = $projects->fetchArray() ) { ?>
					<tr>
						<td><a href="project.php?id=<? echo $project["id"] ?>"><? echo $project["id"] ?></a></td>
						<td><a href="project.php?id=<? echo $project["id"] ?>"><? echo $project["title"] ?></a></td>
					</tr>
<? } ?>
				</tbody>
			</table>
<? } ?>
			</div>
		</div>
		<?php html_footer(); ?>
				<script>
				function projectSave() {
					document.getElementsByTagName("form")[1].submit.click();
				}
		</script>
	</body>
</html>
