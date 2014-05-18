#!/bin/sh
#
# MLTV Database Web Configuration
#
. /usr/lib/slitaz/httphelper

# ====
# Variables
# ====

script="${SCRIPT_NAME}"
path="${script%/*}"
db="/var/tmp/mltv.db"
#script_url="https://chiselapp.com/user/mastersrp/repository/mltv-db"
script_url="http://slitaz:8081"
script_lastid=$(sqlite3 .repo.fossil "SELECT MAX(rid) FROM blob;")
script_rev=$(sqlite3 .repo.fossil "SELECT uuid FROM blob WHERE rid == $script_lastid;")

DEBUG=yes

# ====
# Functions
# ====

[ ! -f "$db" ] && cat schema | sqlite3 $db

html_style() {
	cat << EOT
			body {
				background-color: #ddd;
				margin: 0;
				padding: 0;
			}
			a {
				color: #005;
				text-decoration: none;
			}
			a:hover {
				color: #00b;
			}
			#wrapper {
				background-color: #fff;
				border-bottom: 0.1em solid #55f;
			}
			#content {
				padding: 1em;
			}
			#dashboard {
				border-bottom: 0.1em solid #55f;
			}
			#dashboard form {
				float: right;
				display: inline;
			}
			#sidebar {
				background: #fefefe;
				border: 0.1em solid #ddd;
				min-width: 10em;
				padding: 0.5em;
				float: right;
				display: block;
			}
			pre {
				margin-top: 0;
				background: #f5f5f5;
				border: 0.1em solid #55f;
				border-top: 0.1em solid #555;
				border-radius: 0em 0em 0.5em 0.5em;
				padding: 0.25em;
			}
			pre.header {
				margin-bottom: 0;
				background: #f5f5f5;
				border: 0.±2em solid #555;
				border-bottom: 0;
				border-radius: 0;
				padding: 0.25em;
			}

			#footer {
				text-align: center;
			}
			
			.clear {
				clear: both;
			}

EOT
}

html_header() {
	cat << EOT
<!doctype html>
<html>
	<head>
		<meta charset="utf8">
		<link rel="icon" type="image/png"
			href="logo_traced.png" />
		<title>$TITLE</title>
		<style>
			$(html_style)
		</style>
	</head>
	<body>
		<div id="wrapper">
EOT
}

html_dashboard() {
	cat << EOT
		<div id="dashboard">
			<a href="${script}">Forside</a> |
			<a href="${script}?browse">Gennemse projekter</a> |
			<a href="${script}?create">Opret projekt</a>
			$([ -n "${proj}" ] && echo " | <a href='${script}?delete&amp;p=${proj}'>Slet project</a>")
			<form method="get" action="${script}">
				<input type="text" name="search" placeholder="Søg" />
			</form>
		</div>
		<div class="clear"></div>
		<div id="content">
			<img id="logo" src="logo_traced.png"></img>
			<br />
EOT
}

html_sidebar() {
	cat << EOT
	<div id="sidebar">
		<b>Nyligt oprettede projekter:</b>
		<table>
EOT
		while read proj
		do
			proj_id="$(echo $proj | cut -d '|' -f 1)"
			proj_title="$(echo $proj | cut -d '|' -f 2)"
			[ "${#proj_title}" -gt "40" ] && proj_title="${proj_title:0:37}..."
			cat << EOT
			<tr>
				<td><a href="${script}?view&amp;p=$proj_id">$proj_id</a></td>
				<td><a href="${script}?view&amp;p=$proj_id">$proj_title</a></td>
			</tr>
EOT
	done << EOT
$projects
EOT
	cat << EOT
		</table>
	</div>
EOT
}

html_footer() {
	cat << EOT
			</div>
		</div>
		<div id="footer">
			<p>System og design af <a href="http://necrophcodr.github.io">Steffen Rytter Postas</a>
			Copyright &copy; $(date +%Y) <a href="http://www.middelfart.tv">Middelfart Lokal TV</a></p>
			<small>MLTV-DB revision: <a href="${script_url}/info/${script_rev}">${script_rev}</a></small>
		</div>
	</body>
</html>
EOT
}

# ====
# Routing
# ====

case " $(POST) " in
	*\ create\ *)
		title="$(POST title)"
		desc="$(POST desc)"
		p="$(POST p)"
		music="$(POST music)"
		participants="$(POST participants)"
		producer="$(POST producer)"
		exp_done="$(POST exp_done)"
		exp_length="$(POST exp_length)"
		[ -z "$p" ] && p=NULL
		sqlite3 $db "INSERT INTO projects VALUES ( $p, \"$title\", \"$desc\", $producer, \"$music\", \"$exp_done\", \"$exp_length\", \"$participants\" );"
		local err=$?
		if [ "$err" == "0" ]; then
			[ $p == NULL ] && p=$(sqlite3 $db "SELECT MAX(id) FROM projects;")
			header "Location: ${script}?view&p=$p"
			exit 0
		else
			header
			cat << EOT
$(html_header)
$(html_dashboard)
	<h2>Kunne ikke oprette projekt!</h2>
	<p>Følgende fejlkode blev afgivet af SQLite3: $err</p>
	<p>(mere information om fejlkoder kan findes på <a href="https://sqlite.org/c3ref/c_abort.html">sqlite3.org</a>.)</p>
	<pre class="header">Mener du at dette er en fejl i systemet, så send følgende tekst til system operatøren:
</pre>
	<pre>\$cmd = sqlite3 \$db INSERT INTO projects VALUES( $p, "$title", $producer, "$music", "$exp_done", "$exp_length", "$participants" );<br/>\$err = $err</pre>
$(html_footer)
EOT
			exit 0
		fi
		;;
	*\ delete\ *)
		p=$(POST p)
		sqlite3 $db "DELETE FROM projects WHERE id == $p;"
		local err="$?"
		[ "$err" == "0" ] && header "Location: ${script}"
		header
		cat << EOT
$(html_header)
$(html_dashboard)
	<h4>Kunne ikke slette projekt: $p!</h4>
	<p>SQL fejlkode: $err</p>
$(html_footer)
EOT
		exit 0
		;;
esac

case " $(GET) " in
	*\ create\ *)
		if [ "$(GET create)" == "new" ]; then
			proj="$(GET p)"
			header "Location: ${script}?view&p=${proj}"
			exit 0
		else
			TITLE="Database: Opret projekt"
			header
			html_header
			html_dashboard
			cat << EOT
			<h4>Her har du mulighed for at oprette et nyt projekt</h4>
			<form method="post" action="${script}">
				<input type="hidden" name="create" value="new" />
				<table>
					<tbody>
						<tr>
							<td>Projekt Navn:</td>
							<td><input type="text" name="title" /></td>
						</tr>
						<tr>
							<td>Projekt Nummer:</td>
							<td><input type="text" name="p" placeholder="(nyt)" /></td>
						</tr>
						<tr>
							<td>Producer:</td>
							<td>
								<select name="producer">
									<option value="1">Bent Ove Hansen</option>
								</select>
							</td>
						</tr>
						<tr>
							<td>Beskrivelse</td>
							<td><textarea name="desc"></textarea></td>
						</tr>
						<tr>
							<td>Deltagende:</td>
							<td><textarea name="participants"></textarea></td>
						</tr>
						<tr>
							<td>Musik:</td>
							<td><input type="text" name="music" /></td>
						</tr>
						<tr>
							<td>Forventet færdig:</td>
							<td><input type="datetime-local" name="exp_done" /></td>
						</tr>
						<tr>
							<td>Forventet længde:</td>
							<td><input type="datetime-local" name="exp_length" /></td>
						</tr>
					</tbody>
				</table>
				<input type="submit" value="Opret" />
			</form>
EOT
			html_footer
			exit 0
		fi
		;;
	*\ view\ *)
		proj="$(GET p)"
		TITLE="Database: Vis ${proj}"
		header
		html_header
		html_dashboard

		info=$(sqlite3 $db "SELECT * FROM projects WHERE id == $proj;")

		proj_title="$(echo $info | cut -d '|' -f 2)"
		proj_desc="$(echo $info | cut -d '|' -f 3)"
		proj_producer="$(echo $info | cut -d '|' -f 4)"
		proj_music="$(echo $info | cut -d '|' -f 5)"
		proj_exp_done="$(echo $info | cut -d '|' -f 6)"
		proj_exp_length="$(echo $info | cut -d '|' -f 7)"
		proj_participants="$(echo $info | cut -d '|' -f 8)"

		cat << EOT
		<br />
		proj_title: $proj_title<br/>
		proj_desc: $proj_desc<br/>
		proj_producer: $proj_producer<br/>
		proj_music: $proj_music<br/>
		proj_exp_done: $proj_exp_done<br/>
		proj_exp_length: $proj_exp_length<br/>
		proj_participants: $proj_participants<br/>
EOT

		html_footer
		exit 0
		;;
	*\ delete\ *)
		p="$(GET p)"
		header
		cat << EOT
$(html_header)
$(html_dashboard)
	<h3>Er du sikker på at du vil slette projekt $p?</h3>
	<p><b>ADVARSEL</b>: Følgende handling kan ikke fortrydes, uden system administratorens ekspertise!</p>
	<form action="${script}" method="post">
		<input type="hidden" name="delete" value="delete" />
		<input type="hidden" name="p" value="${p}" />
		<input type="submit" value="Slet" />
	</form>
$(html_footer)
EOT
		;;
	*\ search\ *)
		terms="$(GET search)"
		TITLE="Søg: $terms"
		header
		html_header
		html_dashboard

		results=

		html_footer
		;;
	*\ browse\ *)
		header
		html_header
		html_dashboard
		LIMIT=20
		startid="$(GET startid)"
		[ -z "$startid" ] && startid=$(sqlite3 $db "SELECT MAX(id) FROM projects")
		projects=$(sqlite3 $db "SELECT * FROM projects WHERE id <= $startid ORDER BY id DESC LIMIT $LIMIT")
		while read proj
		do
			proj_id="$(echo $proj | cut -d '|' -f 1 )"
			proj_title="$(echo $proj | cut -d '|' -f 2)"
			cat << EOT
			<a href="${script}?view&amp;p=$proj_id">${proj_id} - ${proj_title}</a>
		<br />	
EOT
		done << EOT
$projects
EOT
		nextid=$(expr $startid - $LIMIT)
		cat << EOT
		<a href="${script}?browse&amp;startid=$nextid">Flere</a>
EOT
		html_footer
		;;
	*)
		# "Dashboard" screen
		TITLE="MLTV - Database"
		projects=$(sqlite3 $db "SELECT * FROM projects ORDER BY id DESC LIMIT 5")
		header
		html_header
		html_dashboard
		html_sidebar $projects
		cat << EOT
		<h2>Velkommen til Middelfart Lokal TV Projekt Databasen.</h2>
		<p>
		Her kan du oprette og se projekter, og slette eksisterende.
		<br />
		Klik blot "<a href="${script}?create">Opret projekt</a>", og du er igang.
		</p>
		<p>
		Du kan gennemse alle projekter ved at klikke på "<a href="${script}?browse">Gennemse projekter</a>" øverst, og ønsker du at søge, kan du blot skrive i søgefeltet og trykke <i>ENTER</i>, for at søge på projektnumre, beskrivelser, titler, og alt andet information.
		</p>
EOT
		html_footer
		;;	
esac
