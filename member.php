<?php
include_once( "lib/core.php" );
?>

<!doctype html>
<html>
	<head>
		<?php html_header($TITLE . " - Forside"); ?>
	</head>
	<body>
		<div id="wrapper">
			<?php html_dashboard(); ?>
			<div id="content">
				<?php html_logo(); ?>
			</div>
		</div>
		<?php html_footer(); ?>
		<script src="js/zepto.min.js"></script>
	</body>
</html>
