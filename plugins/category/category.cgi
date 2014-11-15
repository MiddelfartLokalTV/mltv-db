#!/bin/sh

case " $(GET) " in
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
esac
