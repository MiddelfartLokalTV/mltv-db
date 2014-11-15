#!/bin/sh

case " $(GET) " in
	*\ member\ *)
		member=$(GET id)
		if [ -z "$member" ]; then
			# We're displaying all members
			TITLE="$TITLE - Vis medlemmer"
			header
			html_tmpl 'header'
			html_tmpl 'dashboard'
			cat << EOT
<div id="sidebar">
	<a href="${script}?edit&amp;memid=0">Tilføj medlem</a>
</div>
<h2>Middelfart Lokal TV medlemmer:</h2>
<table>
	<thead>
		<tr>
			<th><b>Navn</b></th>
			<th><b>Telefon</b></th>
			<th><b>E-Mail</b></th>
			<th><b>Antal producerede projekter</b></th>
		</tr>
	</thead>
	<tbody>
EOT
			sqlite3 $db "SELECT id,name,phone,email FROM members ORDER BY name ASC;" | while read member
			do
				member_id=$(echo $member | cut -d '|' -f 1)
				member_name=$(echo $member | cut -d '|' -f 2)
				member_phone=$(echo $member | cut -d '|' -f 3)
				member_email=$(echo $member | cut -d '|' -f 4)
				produced=$(sqlite3 $db "SELECT COUNT(id) FROM projects WHERE producer == $member_id")
				cat << EOT
				<tr>
					<td><a href="${script}?member&amp;memid=$member_id">$member_name</a></td>
					<td>$member_phone</td>
					<td><a href="mailto:$member_email">$member_email</a></td>
					<td><a href="${script}?member&amp;memid=$member_id">$produced</a></td>
				</tr>
EOT
			done
			cat << EOT
			</tbody>
		</table>
EOT
			html_tmpl 'footer'
			exit 0
		else
			member_name=$(sqlite3 $db "SELECT name FROM members WHERE id == $member")
			member_phone=$(sqlite3 $db "SELECT phone FROM members WHERE id == $member")
			member_email=$(sqlite3 $db "SELECT email FROM members WHERE id == $member")
			projects=$(sqlite3 $db "SELECT id FROM projects WHERE producer == $member")

			TITLE="$TITLE - Medlem: $member_name ($member)"
			header
			html_tmpl 'header'
			html_tmpl 'dashboard'
			cat << EOT
<div id="sidebar">
	<a href="${script}?edit&amp;id=$member">Redigér</a><br />
	<a href="${script}?delete&amp;id=$member">Slet</a>
</div>
<h2>$member_name</h2>
<b>Mobil</b>: $member_phone<br/>
<b>E-Mail</b>: <a href="mailto:$member_email">$member_email</a><br/>
<p>${member_name} har produceret følgende:</p>
<table>
	<thead>
		<tr>
			<th>Projekt Nr.</th>
			<th>Projekt Titel</th>
		</tr>
	</thead>
	<tbody>
EOT
			LFS="|"
			for proj in $projects
			do
				project_title=$(sqlite3 $db "SELECT title FROM projects WHERE id == $proj")
				cat << EOT
		<tr>
			<td><a href="${script}?view&amp;p=$proj">$proj</a></td>
			<td><a href="${script}?view&amp;p=$proj">$project_title</a></td>
		</tr>
EOT
			done
			cat << EOT
	</tbody>
</table>
EOT
			html_tmpl 'footer'
			exit 0
		fi
		;;
esac
