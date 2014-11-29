<?php
include_once( "lib/core.php" );
?>

<!doctype html>
<html>
	<head>
		<?php html_header($TITLE . " - Rapport"); ?>
	</head>
	<body>
		<div id="wrapper">
			<?php html_dashboard(); ?>
			<div id="content">
				<?php html_logo(); ?>

				<? if( isset( $_POST["startdate"] ) AND isset( $_POST["enddate"] ) ) { ?>
				<? } else { ?>
					<div id="sidebar">
						<a href="#" onClick="reportCreate();">Opret Rapport</a>
					</div>
					<form action="report.php" method="post">
						<label>Start Dato</label>
							<input type="date" name="startdate" />
						<label>Slut Dato</label>
							<input type="date" name="enddate" />
						<input type="submit" name="submit" style="display:none" />
					</form>
				<? } ?>
			</div>
		</div>
		<?php html_footer(); ?>
<script>
function reportCreate() {
				document.getElementByTagName("form").submit.click();
			}
		</script>
	</body>
</html>
