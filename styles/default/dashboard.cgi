#!/bin/sh
cat << EOT
		<ul id="dashboard">
			<li class="dashbtn"><a href="${script}">Forside</a></li>
			<li class="dashbtn"><a href="${script}?member">Medlemmer</a></li>
			<li class="dashbtn"><a href="${script}?category">Kategorier</a></li>
			<li class="dashbtn"><a href="${script}?browse">Gennemse projekter</a></li>
			<li class="dashbtn"><a href="${script}?edit">Opret projekt</a></li>
			<li class="dashbtn"><a href="${script}?report">Opret Rapport</a></li>
			<li class="dashbtn"><form method="get" action="${script}">
				<input type="text" name="search" placeholder="Søg" />
			</form></li>
		</ul>
		<div class="clear"></div>
		<div id="content">
			<div id="header">
				<a href="${script}"><img id="logo" src="logo.gif" /></a>
				$([ -n "$(GET view)" ] && [ -n "$(GET p)" ] && echo '<h2>Arbejdskort</h2>')
			</div>
			<br />
EOT
