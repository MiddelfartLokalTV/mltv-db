<?php
include_once( "lib/core.php" );

if( isset( $_POST["category"] ) ) {
	$cat = $_POST["category"];
	$db->exec( "INSERT INTO categories VALUES( NULL, '" . $cat . "' )" );
}
?>

<!doctype html>
<html>
	<head>
		<?php html_header($TITLE . " - Kategorier"); ?>
	</head>
	<body>
		<div id="wrapper">
			<?php html_dashboard(); ?>
			<div id="content">
				<?php 
				html_logo();
				$categories = $db->query( "SELECT * FROM categories" );
				while( $category = $categories->fetchArray() ) { ?>
	<a href="project.php&amp;cat=<?php echo $category['id'] ?>"><?php echo htmlentities($category['name'])?></a>
			<?php	} ?>
			<form action="category.php" method="post">
				<input type="text" name="category" placeholder="Ny" />
				<input type="submit" value="Opret" />
			</form>
			</div>
		</div>
		<?php html_footer(); ?>
		<script src="js/zepto.min.js"></script>
	</body>
</html>
