<?php
include_once( "lib/core.php" );

$page = new Page( "default" );

$page->Render( "header", array("title" => "MLTV - Forside") );

$page->Render( "logo", [] );

html_logo();

$page->Render( "sidebar", [] );

?>

				<h2>Velkommen til Middelfart Lokal TV Projekt Databasen</h2>
				<p>
				Her kan du oprette og se projekter.
				<br />
				Klik blot <a href="project.php?edit">Opret Projekt</a>, og du er igang.
				</p>
				<p>
				Du kan gennemse alle projekter ved at klikke på <a href="project.php">Gennemse  Projekter</a> øverst, og ønsker du at søge, kan du blot skrive i søgefeltet og trykke <code>ENTER</code>, for at søge på projektnumre, beskrivelser, titler, og alt andet information.
				</p>


<?php $page->Render( "footer", [] ) ?>

