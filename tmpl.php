<?php
include_once( "lib/core.php" );
$page = new Page( "default" );
$page->Render( "header", array( "title" => "MLTV - Forside" ) );
$page->Render( "logo", [] );
?>

<h2>Hello, World!</h2>

<? $page->Render( "footer", [] ); ?>

