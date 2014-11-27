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
				<?php html_logo(); html_sidebar(); ?>
				<h2>Velkommen til Middelfart Lokal TV Projekt Databasen</h2>
				<p>
				Her kan du oprette og se projekter.
				<br />
				Klik blot <a href="project.php?edit">Opret Projekt</a>, og du er igang.
				</p>
				<p>
				Du kan gennemse alle projekter ved at klikke på <a href="project.php">Gennemse  Projekter</a> øverst, og ønsker du at søge, kan du blot skrive i søgefeltet og trykke <code>ENTER</code>, for at søge på projektnumre, beskrivelser, titler, og alt andet information.
				</p>
			</div>
		</div>
		<?php html_footer(); ?>
	</body>
</html>
