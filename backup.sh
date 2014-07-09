#!/bin/sh
# Automated backup of database

# Ensure the script is only executed by root, and NO ONE ELSE!
[ "$(id -u)" == "0" ] || exit 0

check_bin() {
	bin="${1}"
	if [[ -z "$(which ${bin})" ]]; then
		echo "You need \"${bin}\" installed!"
		exit 0
	fi
}

# Check for required applications
check_bin zpaq

# Initialize variables from index.cgi
. index.cgi >/dev/null
backup="/usr/lib/mltv"

# Perform the actual backup
mkdir -p "${backup}"
zpaq a ${backup}/db.zpaq "${db}"
