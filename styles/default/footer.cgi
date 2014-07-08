#!/bin/sh
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
