#!/bin/sh
cat << EOT
<!doctype html>
<html>
	<head>
		<meta charset="utf8">
		<link rel="icon" type="image/png"
			href="logo_traced.png" />
		<title>$TITLE</title>
		<style>
		$(cat ${styles}/${STYLE}/style.css)
		</style>
	</head>
	<body>
		<div id="wrapper">
		<!-- content starts here -->
EOT
