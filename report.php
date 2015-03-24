<?php
include_once( "lib/core.php" );

$page = new Page( "default" );
$page->Render( "header", "MLTV - Rapport" );
$page->Render( "logo", [] );
if( isset( $_POST["startdate"] ) AND isset( $_POST["enddate"] ) ) {
				$projects = $db->query( "SELECT * FROM projects WHERE release BETWEEN '" . $_POST["startdate"] . "' AND '" . $_POST["enddate"] . "'" );

				while ( $project = $projects->fetchArray() ) {
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
						$producer				= $db->querySingle( "SELECT name FROM members WHERE id == ".$proj_producer );
						$editor					= $db->querySingle( "SELECT name FROM members WHERE id == ".$proj_editor );
						$category				= $db->querySingle( "SELECT name FROM categories WHERE id == ".$proj_cat );
						$release_type		= $db->querySingle( "SELECT type FROM release_type WHERE id == ".$proj_rel_type );

?>
					<h3><? echo $proj ?>&nbsp; - &nbsp; <? echo $proj_title ?></h3>

					<table id="project-view">
						<tr>
						<td><b>Producer</b>: <a href="member.php?id=<? echo $proj_producer ?>"><?echo $producer ?></a></td>
							<td><b>Oprettet</b>: <? echo $proj_created ?></td>
						</tr>
						<tr>
							<td><b>Kategori</b>: <a href="project.php?cat=<? echo $proj_cat ?>"><? echo $category ?></a></td>
							<td><b>Redigering</b>: <a href="member.php?id=<? echo $proj_editor ?>"><? echo $editor ?></a></td>
						</tr>
						<tr>
							<td><b>Udgivet</b>: <? echo $proj_release ?></td>
							<td><b>Aktuel Længde</b>: <? echo $proj_real_len ?></td>
						</tr>
						<tr>
							<td><b>Tidsramme</b>: <? echo $proj_timespan ?></td>
							<td><b>Udgivelsestype</b>: <? echo $release_type ?></td>
						</tr>
					</table>
				<?} } else { ?>
					<div id="sidebar">
						<a href="#" onClick="reportCreate();">Opret Rapport</a>
					</div>
					<form id="form_report" action="report.php" method="post">
						<label>Start Dato</label>
							<input type="date" name="startdate" />
						<label>Slut Dato</label>
							<input type="date" name="enddate" />
						<input type="submit" name="submit" style="display:none" />
					</form>
				<? } ?>
			</div>
		</div>
<?php $page->Render( "footer", [] ) ?>
