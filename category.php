<?php
include_once( "lib/core.php" );

if( isset( $_POST["category"] ) ) {
	$cat = $_POST["category"];
	$db->exec( "INSERT INTO categories VALUES( NULL, '" . $cat . "' )" );
	header( "Location: category.php" );
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
	<a href="project.php?cat=<?php echo $category['id'] ?>"><?php echo htmlentities($category['name'])?></a> <br/>
			<?php	} ?>
			<form action="category.php" method="post">
				<input type="text" name="category" placeholder="Ny" />
				<input type="submit" value="Opret" />
			</form>
			</div>
		</div>
		<?php html_footer(); ?>
	</body>
</html>
