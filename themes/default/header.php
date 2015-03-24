<?php
global $TITLE;
global $page;
if( $TITLE === null ) { $TITLE = "Unnamed"; }
?>
<!doctype html>
<html>
	<head>
		<meta charset="utf-8">
			<link rel="stylesheet" href="css/style.css" />
			<link rel="icon" type="image/png" href="logo_traced.png" />
			<title><?php echo $TITLE ?></title>
	</head>
	<body>
		<div id="wrapper">
			<?php $page->Render( 'dashboard' ) ?>
			<div id="content">
<?php
?>
