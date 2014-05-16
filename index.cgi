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

# ====
# Functions
# ====

[ ! -f "$db" ] && cat schema | sqlite3 $db

html_header() {
	cat << EOT
<!doctype html>
<html>
	<head>
		<meta charset="utf8">
		<title>$TITLE</title>
		<style>
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
			#content {
				background-color: #fff;
				border-bottom: 0.1em solid #55f;
			}
			#dashboard {
				border-bottom: 0.1em solid #55f;
			}
			#dashboard form {
				float: right;
				display: inline;
			}
			#footer {
				text-align: center;
			}
			
			.clear {
				clear: both;
			}
		</style>
	</head>
	<body>
		<div id="content">
EOT
}

html_dashboard() {
	cat << EOT
		<div id="dashboard">
			<a href="${script}">Forside</a>
			<a href="${script}?create">Opret projekt</a>
			$([ -n "${proj}" ] && echo " | <a href='${script}?delete&amp;p=${proj}'>Slet project</a>")
			<form method="get" action="${script}">
				<input type="text" name="search" />
			</form>
		</div>
		<div class="clear"></div>
EOT
}

html_footer() {
	cat << EOT
		</div>
		<div id="footer">
			<p>System og design af <a href="http://necrophcodr.github.io">Steffen Rytter Postas</a></p>
			<p>Copyright &copy; $(date +%Y) <a href="http://www.middelfart.tv">Middelfart Lokal TV</a></p>
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
		title="$(GET title)"
		p="$(GET p)"
		music="$(GET music)"
		producer="$(GET producer)"
		exp_done="$(GET exp_done)"
		exp_length="$(GET exp_length)"
		[ -z "$p" ] && p="NULL"
		sqlite3 $db "INSERT INTO projects VALUES ( $p, \"$title\", $producer, \"$music\", \"$exp_done\", \"$exp_length\", \"$participants\" );"
		local err=$?
		if [ "$err" == "0" ]; then
			header "Location: ${script}?view&p=$p"
			exit 0
		else
			cat << EOT
$(html_header)
$(html_dashboard)
	<h2>Kunne ikke oprette projekt!</h2>
	<p>Følgende fejlkode blev afgivet af SQLite3: $err</p>
	<p>(mere information om fejlkoder kan findes på sqlite3.org</p>
$(html_footer)
EOT
			exit 0
		fi
		;;
	*\ delete\ *)
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
			<h4>Her har du muligheden for at oprette et nyt projekt</h4>
			<form method="get" action="${script}">
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
		html_footer
		exit 0
		;;
	*)
		# "Dashboard" screen
		TITLE="MLTV - Database"
		header
		html_header
		html_dashboard
		cat << EOT
		<h2>Velkommen til Middelfart Lokal TV Projekt Databasen.</h2>
		<p>
		Her kan du oprette og se projekter, og slette eksisterende.
		<br />
		Klik blot "Opret projekt", og du er igang.
		</p>
EOT
		html_footer
		exit 0
		;;	
esac
