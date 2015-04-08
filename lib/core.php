<?php
$TITLE = "MLTV";
$DB = "/tmp/mltv.db";

$db = new SQLite3( $DB );
$db->exec( fread( fopen( "schema", 'r' ), filesize( 'schema' ) ) );

class Page {
	private $template;

	public function __construct( $theme ) {
		$this->template = $theme;
	}
	
	public function Render( $page, $opts ) {
		$OPTS = [];
		if( $opts != null ) {
			foreach( $opts as $key => $value ) {
				$OPTS[$key] = $value;
			}
		}
		$filename = "themes/".$this->template."/".$page;
		if( fopen( $filename, 'r' ) ) {
			$size = filesize( $filename );
			if( $size <= 0 ) { return 0; }
			$file = fopen( $filename, 'r' );
			$content = fread( $file, $size );
			fclose( $file );
			echo $content;
			return 0;
		}
		if( fopen( $filename.".php", 'r' ) ) {
			include $filename.".php";
			return 0;
		}
		return 1;
	}
}

?>
