#!/bin/sh

# Automated backup of database

[ "$(id -u)" == "0" ] || exit 0

db="/var/tmp/mltv.db"
backup="/usr/lib/mltv"

mkdir -p "${backup}"
zpaq a ${backup}/db.zpaq "${db}"
