#!/bin/sh

case " $(GET) " in
	*\ report\ *)
		TITLE="$TITLE - Rapport"
		header
		html_tmpl "header"
		html_tmpl "dashboard"
		proj_latest_id=$(sqlite3 $db "SELECT MAX(id) FROM projects")
		proj_latest_date=$(sqlite3 $db "SELECT release FROM projects WHERE id == $proj_latest_id")
		proj_oldest_date=$(sqlite3 "SELECT date(\"$proj_latest_date\", \"-3 months\");" )
		proj_count=$(sqlite3 $db "SELECT id FROM projects WHERE release == \"$proj_oldest_date\"")
		echo $proj_oldest_date
		for id in $(seq $proj_count $proj_latest_id); do
			echo $id
		done
		html_tmpl "footer"
		exit 0
		;;
esac

