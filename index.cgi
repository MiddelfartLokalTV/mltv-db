#!/bin/sh
#
# MLTV Database Web Configuration
#
. /usr/lib/slitaz/httphelper

TITLE="MLTV"

# ====
# Variables
# ====

root="$(pwd)"
styles="${root}/styles"
script="${SCRIPT_NAME}"
path="${script%/*}"
db="/var/tmp/mltv.db"
script_url="https://chiselapp.com/user/mastersrp/repository/mltv-db"
#script_url="http://${HTTP_HOST%:*}:8082"
script_lastid=$(sqlite3 .repo.fossil "SELECT MAX(rid) FROM blob;")
script_rev=$(sqlite3 .repo.fossil "SELECT uuid FROM blob WHERE rid == $script_lastid;")

STYLE="default"
DEBUG=yes
PLUGINS="${root}/plugins"

# Ensure database exists.
[ ! -f "$db" ] && cat schema | sqlite3 $db

# ====
# Functions
# ====

# Ensure that problematic inserts doesn't exist.
sanitize() {
	sed -e 's|\&|\&amp;|g; s|<|\&lt;|g; s|>|\&gt;|g; s|\"|\&quot;|g'
}

html_tmpl() {
	tmpl="$1"
	if [[ -f "${styles}/${STYLE}/${tmpl}.cgi" ]]; then
		. ${styles}/${STYLE}/${tmpl}.cgi
	fi
}

html_display_error() {
	cat << EOT
	<h2>Kunne ikke fuldføre din anmodning!</h2>
	<p>Følgende fejlkode blev afgivet af SQLite3: $err</p>
	<p>(mere information om fejlkoder kan findes på <a href="https://sqlite.org/c3ref/c_abort.html">sqlite3.org</a>.)</p>
	<pre class="header">Mener du at dette er en fejl i systemet, så send følgende tekst til system operatøren:
</pre>
	<pre>\$cmd = sqlite3 \$db $sql<br/>\$err = $err</pre>

EOT
}

html_sidebar() {
	cat << EOT
	<div id="sidebar">
		<b>Nyligt oprettede projekter:</b>
		<table>
EOT
		sqlite3 $db "SELECT id,title FROM projects ORDER BY id DESC LIMIT 15" |	while read proj
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
	done
	cat << EOT
		</table>
	</div>
EOT
}

html_select_members() {
	edit_member="$1"
	sqlite3 $db 'SELECT id,name FROM members ORDER BY name ASC' | while read member
	do
		mem_id="$(echo $member | cut -d '|' -f 1 )"
		mem_name="$(echo $member | cut -d '|' -f 2)"
		if [ "$edit_member" -eq "$mem_id" ]; then
			echo "<option selected=selecte±d value=$mem_id>$mem_name</option>"
		else
			echo "<option value=$mem_id>$mem_name</option>"
		fi
	done
}

html_select_categories() {
	edit_category="$1"
	sqlite3 $db 'SELECT * FROM categories' | while read category
	do
		cat_id="$(echo $category | cut -d '|' -f 1)"
		cat_name="$(echo $category | cut -d '|' -f 2)"
		if [ "$edit_category" -eq "$cat_id" ]; then
			echo "<option selected=selected value=\"$cat_id\">$cat_name</option>"
		else
			echo "<option value=$cat_id>$cat_name</option>"
		fi
	done
}

# ====
# Plugin support
# ====

for plugin in $(ls $PLUGINS); do
	[[ -f "$PLUGINS/${plugin}/${plugin}.cgi" ]] && . $PLUGINS/${plugin}/${plugin}.cgi
done

# ====
# Routing
# ====

case " $(POST) " in
	*\ save\ *)
		if [ "$(POST save)" == "category" ]; then
			# We're just creating a new category, let's get it over with quick
			category="$(POST category)"
			sql="INSERT INTO categories VALUES( NULL, \"$category\");"
			redir="Location: ${script}?category"
		elif [ "$(POST save)" == "member" ]; then
			name="$(POST name | sanitize)"
			phone="$(POST phone | sanitize)"
			email="$(POST email | sanitize)"
			memid="$(POST memid)"
			if [ "$memid" == "NULL" ]; then
				# We're adding a new member
				sql="INSERT INTO members VALUES( NULL, \"$name\", \"$phone\", \"$email\");"
				redir="Location: ${script}?member"
			else
				# We're updating an existing member
				sql="UPDATE members SET name=\"$name\", phone=\"$phone\", email=\"$email\" WHERE id == $memid"
				redir="Location: ${script}?member&id=$memid"
			fi
		elif [ "$(POST save)" == "project" ]; then
			title="$(POST title | sanitize)"
			desc="$(POST desc | sanitize)"
			p="$(POST p)"
			producer="$(POST producer)"
			editor="$(POST editor)"
			category=$(POST category)
			music="$(POST music | sanitize)"
			created="$(POST created | sanitize)"
			exp_done="$(POST exp_done | sanitize)"
			exp_length="$(POST exp_length | sanitize)"
			real_length="$(POST real_length | sanitize)"
			release="$(POST release | sanitize)"
			participants="$(POST participants | sanitize)"
			if [ -z "$p" ]; then
				# We're creating a new project
				[ -z "$p" ] && p=NULL
				sql="INSERT INTO projects VALUES ( $p, \"$title\", \"$desc\", $producer, $editor, $category, \"$music\", \"$created\", \"$exp_done\", \"$exp_length\", \"$real_length\", \"$release\", \"$participants\" );"
				realp=$(sqlite3 $db "SELECT MAX(id) FROM projects")
				realp=$(($realp + 1 ))
				redir="Location: ${script}?view&p=$realp"
			elif [ -z "$(sqlite3 $db 'SELECT id FROM projects WHERE id == '$p)" ]; then
				# We're creating a new project with id $p
				sql="INSERT INTO projects VALUES ( $p, \"$title\", \"$desc\", $producer, $editor, $category, \"$music\", \"$created\", \"$exp_done\", \"$exp_length\", \"$real_length\", \"$release\", \"$participants\" );"
				redir="Location: ${script}?view&p=$p"
			else
				# We're updating an existing project
				sql="UPDATE projects SET title = \"$title\", desc = \"$desc\", producer = $producer, editor = $editor, category = $category, music = \"$music\", created = \"$created\", expected_done = \"$exp_done\", expected_length = \"$exp_length\", real_length = \"$real_length\", release = \"$release\", participants = \"$participants\" WHERE id == $p;"
				redir="Location: ${script}?view&p=$p"
			fi
		else
			header "Location: $HTTP_REFERER"
			exit 0
		fi
		sqlite3 $db "$sql"
		local err=$?
		if [ "$err" == "0" ]; then
			header "$redir"
			exit 0
		else
			header
			html_tmpl 'header'
			html_tmpl 'dashboard'
			html_display_error
			html_tmpl 'footer'
			exit 0
		fi
		;;
	*\ delete\ *)
		if [ "$(POST delete)" == "category" ]; then
			# We're just deleting a category, let's get it over with quick
			category=$(POST category)
			sql="DELETE FROM categories WHERE id == $category"
			redir="Location: ${script}?category"
		elif [ "$(POST delete)" == "member" ]; then
			# We're just deleting a member, let's get it over with quick
			member=$(POST memid)
			sql="DELETE FROM members WHERE id == $member"
			redir="Location: ${script}?member"
		else
			header "Location: $HTTP_REFERER"
			exit 0
		fi
		sqlite3 $db "$sql"
		local err="$?"
		[ "$err" == "0" ] && header "$redir"
		header
		TITLE="$TITLE - SQL Fejl!"
		html_tmpl 'header'
		html_tmpl 'dashboard'
		html_display_error
		html_tmpl 'footer'
		exit 0
		;;
esac

case " $(GET) " in
	*\ edit\ *)
		proj=$(GET p)
		member=$(GET memid)
		if [ -n "$member" ] ; then
			member_name=$(sqlite3 $db "SELECT name FROM members WHERE id == $member")
			member_phone=$(sqlite3 $db "SELECT phone FROM members WHERE id == $member")
			member_email=$(sqlite3 $db "SELECT email FROM members WHERE id == $member")
			if [ "$member" -eq "0" ]; then
				member=NULL
				TITLE="$TITLE - Opret nyt medlem"
			else
				TITLE="$TITLE - Redigér medlem: $member_name ($member)"
			fi
			header
			html_tmpl 'header'
			html_tmpl 'dashboard'
			cat << EOT
<form action="${script}" method="post">
	<input type="hidden" name="save" value="member" />
	<input type="hidden" name="memid" value="$member" />
	<table>
		<tbody>
			<tr>
				<td><b>Navn</b>:</td>
				<td><input type="text" name="name" value="$member_name" /></td>
			</tr>
			<tr>
				<td><b>Telefon</b>:</td>
				<td><input type="text" name="phone" value="$member_phone" /></td>
			</tr>
			<tr>
				<td><b>E-Mail</b>:</td>
				<td><input type="email" name="email" value="$member_email" /></td>
			</tr>
		</tbody>
	</table>
	<input type="submit" value="Gem" />
</form>
EOT
			html_tmpl 'footer'
			exit 0
		elif [ -z "$proj" ]; then
			TITLE="Database: Opret projekt"
		else
			TITLE="Database: Rediger project - $proj"
			proj_title=$(sqlite3 $db "SELECT title FROM projects WHERE id == $proj")
			proj_desc=$(sqlite3 $db "SELECT desc FROM projects WHERE id == $proj")
			proj_producer=$(sqlite3 $db "SELECT producer FROM projects WHERE id == $proj")
			proj_editor=$(sqlite3 $db "SELECT editor FROM projects WHERE id == $proj")
			proj_category=$(sqlite3 $db "SELECT category FROM projects WHERE id == $proj")
			proj_music=$(sqlite3 $db "SELECT music FROM projects WHERE id == $proj")
			proj_created=$(sqlite3 $db "SELECT created FROM projects WHERE id == $proj")
			proj_exp_done=$(sqlite3 $db "SELECT expected_done FROM projects WHERE id == $proj")
			proj_exp_length=$(sqlite3 $db "SELECT expected_length FROM projects WHERE id == $proj")
			proj_real_length=$(sqlite3 $db "SELECT real_length FROM projects WHERE id == $proj")
			proj_release=$(sqlite3 $db "SELECT release FROM projects WHERE id == $proj")
			proj_participants=$(sqlite3 $db "SELECT participants FROM projects WHERE id == $proj")
		fi
		header
		html_tmpl 'header'
		html_tmpl 'dashboard'
		cat << EOT
		<div id="sidebar">
		<a href="#" onClick="projectSave();">Gem</a>
		</div>
		<form method="post" action="${script}">
			<input type="hidden" name="save" value="project"/>
			<table>
				<tbody>
					<tr>
						<td>Projekt Navn:</td>
						<td><input type="text" name="title" value="$proj_title" /></td>
					</tr>
					<tr>
						<td>Projekt Nummer:</td>
EOT
		if [[ -z "$proj" ]]; then
			cat << EOT
			<td><input type="text" name="p" placeholder="nyt" disabled="disabled" /> <i>(projekt nummer tildeles efter oprettelse)</i></td>
EOT
		else
			cat << EOT
						<td><input type="text" name="p" placeholder="(nyt)" value="$proj" /></td>
EOT
		fi
		cat << EOT
					</tr>
					<tr>
						<td>Producer:</td>
						<td>
							<select name="producer">
								$(html_select_members $proj_producer)
							</select>
						</td>
					</tr>
					<tr>
						<td>Oprettet:</td>
						<td><input type="date" name="created" value="$proj_created" /></td>
					</tr>
					<tr>
						<td>Redigering:</td>
						<td>
							<select name="editor">
								$(html_select_members $proj_editor)
							</select>
						</td>
					</tr>
					<tr>
						<td>Kategori</td>
						<td>
							<select name="category">
								$(html_select_categories $proj_category)
							</select>
						</td>
					</tr>
					<tr>
						<td>Beskrivelse til YouTube:</td>
						<td><textarea cols="80" rows="12" name="desc">${proj_desc}</textarea></td>
					</tr>
					<tr>
						<td>Deltagende:</td>
						<td><textarea name="participants">${proj_participants}</textarea></td>
					</tr>
					<tr>
						<td>Musik:</td>
						<td><input type="text" name="music" value="${proj_music}" /></td>
					</tr>
					<tr>
						<td>Forventet færdig:</td>
						<td><input type="date" name="exp_done" value="${proj_exp_done}" /></td>
					</tr>
					<tr>
						<td>Forventet længde: (TT:MM:SS)</td>
						<td><input type="text" name="exp_length" value="${proj_exp_length}" /></td>
					</tr>
					<tr>
						<td>Udgivet:</td>
						<td><input type="date" name="release" value="${proj_release}" /></td>
					</tr>
					<tr>
						<td>Aktuel længde: (TT:MM:SS)</td>
						<td><input type="text" name="real_length" value="${proj_real_length}" /></td>
					</tr>
				</tbody>
			</table>
			<input type="submit" name="submit" style="display: none;" />
		</form>
EOT
		html_tmpl 'footer'
		exit 0
		;;
	*\ delete\ *)
		p="$(GET p)"
		member="$(GET memid)"
		cat="$(GET cat)"
		if [ -n "$member" ]; then
			msg="Er du sikker på du vil slette medlem: $member?"
			val="member"
			html="<input type='hidden' name='memid' value=\"${member}\" />"
			TITLE="$TITLE - Slet medlem $member?"
		elif [ -n "$cat" ]; then
			msg="Er du sikker på du vil slette kategori $cat?"
			val="category"
			html="<input type='hidden' name='category' value=\"${cat}\" />"
			TITLE="$TITLE - Slet kategori $cat?"
		else
			header "Location: $HTTP_REFERER"
			exit 0
		fi
		header
		html_tmpl 'header'
		html_tmpl 'dashboard'
		cat << EOT
	<h3>$msg</h3>
	<p><b>ADVARSEL</b>: Følgende handling kan ikke fortrydes, uden system administratorens ekspertise!</p>
	<form action="${script}" method="post">
		<input type="hidden" name="delete" value="$val" />
		$html
		<input type="submit" value="Slet" />
	</form>
EOT
		html_tmpl 'footer'
		;;
	*\ category\ *)
		header
		TITLE="$TITLE - Vis kategorier"
		html_tmpl 'header'
		html_tmpl 'dashboard'
		LFS="|"
		sqlite3 $db "SELECT id FROM categories" | while read cat
		do
			cat_name=$(sqlite3 $db "SELECT name FROM categories WHERE id == $cat")
			cat << EOT
$(btn_del "cat" "$cat")
<a href="${script}?browse&amp;cat=$cat">$cat_name</a>
<br />
EOT
		done
		cat << EOT
<form action="${script}" method="post">
	<input type="hidden" name="save" value="category" />
	<input type="text" name="category" placeholder="Ny" />
	<input type="submit" value="Opret" />
EOT
		html_tmpl 'footer'
		exit 0
		;;
	*\ view\ *)
		proj="$(GET p)"
		TITLE="$TITLE - Database: Vis ${proj}"
		header
		html_tmpl 'header'
		html_tmpl 'dashboard'

		proj_title=$(sqlite3 $db "SELECT title FROM projects WHERE id == $proj;")
		proj_desc=$(sqlite3 $db "SELECT desc FROM projects WHERE id == $proj")
		proj_producer_id=$(sqlite3 $db "SELECT producer FROM projects WHERE id == $proj")
		proj_producer=$(sqlite3 $db "SELECT name FROM members WHERE id == $proj_producer_id")
		proj_editor=$(sqlite3 $db "SELECT editor FROM projects WHERE id == $proj")
		proj_editor_name=$(sqlite3 $db "SELECT name FROM members WHERE id == $proj_editor")
		proj_category_id=$(sqlite3 $db "SELECT category FROM projects WHERE id == $proj")
		proj_category=$(sqlite3 $db "SELECT name FROM categories WHERE id == $proj_category_id")
		proj_music=$(sqlite3 $db "SELECT music FROM projects WHERE id == $proj")
		proj_created=$(sqlite3 $db "SELECT created FROM projects WHERE id == $proj")
		proj_exp_done=$(sqlite3 $db "SELECT expected_done FROM projects WHERE id == $proj")
		proj_exp_length=$(sqlite3 $db "SELECT expected_length FROM projects WHERE id == $proj")
		proj_real_length=$(sqlite3 $db "SELECT real_length FROM projects WHERE id == $proj")
		proj_release=$(sqlite3 $db "SELECT release FROM projects WHERE id == $proj")
		proj_participants=$(sqlite3 $db "SELECT participants FROM projects WHERE id == $proj")

		if [ -z "$proj_producer" ]; then
			proj_producer="(ukendt)"
		else
			proj_producer="<a href=\"${script}?member&amp;id=$proj_producer_id\">$proj_producer</a>"
		fi
		if [ -z "$proj_editor_name" ]; then
			proj_editor="ukendt eller ingen ($proj_editor)"
		else
			proj_editor="<a href=\"${script}?member&amp;id=$proj_editor\">$proj_editor_name</a>"
		fi

		cat << EOT
		<div id="sidebar">
			<a href="${script}?edit&amp;p=$proj">Redigér</a>
		</div>
		<h3>$proj &nbsp; - &nbsp; $proj_title</h3>
		<table id="project-view">
			<tr>
				<td><b>Producer</b>: $proj_producer</td>
				<td><b>Oprettet</b>: $proj_created</td>
			</tr>
			<tr>
				<td><b>Kategori</b>: <a href="${script}?browse&amp;cat=$proj_category_id">$proj_category</a></td>
				<td><b>Redigering</b>: $proj_editor</td>
			</tr>
			<tr>
				<td><b>Beskrivelse</b>:
EOT
		echo "${proj_desc}" | while read desc
		do
			echo "${desc}<br/>"
		done
		cat << EOT
				</td>
				<td></td>
			<tr>
				<td><b>Musik</b>: $proj_music</td>
				<td><b>Deltagere</b>: $proj_participants</td>
			</tr>
			<tr>
				<td><b>Forventet færdig</b>: $proj_exp_done</td>
				<td><b>Forventet længde</b>: $proj_exp_length</td>
			</tr>
			<tr>
				<td><b>Udgivet</b>: $proj_release</td>
				<td><b>Aktuel længde</b>: $proj_real_length</td>
			</tr>
		</table>
EOT

		html_tmpl 'footer'
		exit 0
		;;
	*\ browse\ *)
		category="$(GET cat)"
		startid="$(GET startid)"
		maxid=$(sqlite3 $db "SELECT MAX(id) FROM projects")
		minid=$(sqlite3 $db "SELECT MIN(id) FROM projects")
		LIMIT=20
		[ -z "$startid" ] && startid=$maxid

		nextid=$(expr $startid - $LIMIT)
		previd=$(expr $startid + $LIMIT)
		if [ "$startid" -gt "$maxid" ] || [ "$startid" == "$maxid" ]; then
		 startid=$maxid
		 previd=$maxid
		fi
		if [ "$startid" -lt "$minid" ] || [ "$startid" == "$minid" ]; then
			startid=$(expr $minid + $LIMIT)
			nextid=$minid
		fi
		if [ -n "${category}" ]; then
			# User wants to see projects in $category
			projects=$(sqlite3 $db "SELECT id,title FROM projects WHERE id <= $startid AND category == $category ORDER BY id DESC LIMIT $LIMIT")
			TITLE="$TITLE - Database: Gennemse $category"
		else
			# User wants to see ALL projects
			projects=$(sqlite3 $db "SELECT id,title FROM projects WHERE id <= $startid ORDER BY id DESC LIMIT $LIMIT")
			TITLE="$TITLE - Database: Gennemse alle"
		fi
		header
		html_tmpl 'header'
		html_tmpl 'dashboard'
		categories=$(sqlite3 $db "SELECT * FROM categories")
		if [ -n "${categories}" ]; then
			echo "<div id='sidebar'>"
			while read cat
			do
				cat_id="$(echo $cat | cut -d '|' -f 1)"
				cat_name="$(echo $cat | cut -d '|' -f 2)"
				cat << EOT
			<a href="${script}?browse&amp;cat=$cat_id">$cat_name</a><br />
EOT
			done << EOT
$categories
EOT
			echo "</div>"
		fi
		cat << EOT
	<table>
		<thead>
			<tr>
				<th>Projekt nr.</th>
				<th>Projekt titel</th>
			</tr>
		</thead>
		<tbody>
EOT
		while read proj
		do
			proj_id="$(echo $proj | cut -d '|' -f 1 )"
			proj_title="$(echo $proj | cut -d '|' -f 2)"
			cat << EOT
			<tr>
				<td><a href="${script}?view&amp;p=$proj_id">${proj_id}</a></td>
				<td><a href="${script}?view&amp;p=$proj_id">${proj_title}</a></td>
			</tr>
EOT
		done << EOT
$projects
EOT
		cat << EOT
		</tbody>
	</table>
		<a href="${script}?browse&amp;startid=$nextid">Ældre</a> | <a href="${script}?browse&amp;startid=$previd">Nyere</a>
EOT
		html_tmpl 'footer'
		;;
	*\ search\ *)
		terms="$(GET search)"
		TITLE="$TITLE - Søg: $terms"
		header
		html_tmpl 'header'
		html_tmpl 'dashboard'
		cat << EOT
		<table>
EOT

		sqlite3 $db "SELECT id,title FROM projects WHERE id LIKE \"%$terms%\" OR title LIKE \"%$terms%\" OR desc LIKE \"%$terms%\" OR music LIKE \"%$terms%\" OR participants LIKE \"%$terms%\" ORDER BY id DESC" | while read result
		do
			result_id="$(echo $result | cut -d '|' -f 1)"
			result_title="$(echo $result | cut -d '|' -f 2)"
			cat << EOT
			<tr>
				<td><a href="${script}?view&amp;p=$result_id">$result_id</a></td>
				<td><a href="${script}?view&amp;p=$result_id">$result_title</a></td>
			</tr>

EOT
		done
		cat << EOT
	</table>
EOT
		html_tmpl 'footer'
		;;
	*)
		# "Dashboard" screen
		TITLE="$TITLE - Database"
		header
		html_tmpl 'header'
		html_tmpl 'dashboard'
		html_sidebar $projects
		cat << EOT
		<h2>Velkommen til Middelfart Lokal TV Projekt Databasen.</h2>
		<p>
		Her kan du oprette og se projekter, og slette eksisterende.
		<br />
		Klik blot "<a href="${script}?edit">Opret projekt</a>", og du er igang.
		</p>
		<p>
		Du kan gennemse alle projekter ved at klikke på "<a href="${script}?browse">Gennemse projekter</a>" øverst, og ønsker du at søge, kan du blot skrive i søgefeltet og trykke <code>ENTER</code>, for at søge på projektnumre, beskrivelser, titler, og alt andet information.
		</p>
EOT
		html_tmpl 'footer'
		;;	
esac
