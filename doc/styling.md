# Styling and templates

The MLTV database has been written to support the usage of external themes and styles.  
The functionality of this is pretty simple. Each template is simply a CGI script, and these CGI scripts can do exactly whatever they want to as long as the following criteria are met:

 1. There are the following templates present in a style: header.cgi, footer.cgi.
 2. header.cgi implements the <head> section, and begins with <html>.
 3. footer.cgi implements the end of the <html> section, as well as anything in between.

With these criteria met, the style should function pretty much perfectly. There might be certain exceptions to this. If you wish to be sure, follow this guide exactly to ensure that you do not break anything.  
This is especially a good idea if you are new to this kind of system.  
To create a new style, the following method is prefered for beginners:  
  
 1. Make a copy of the styles/default directory in the styles directory.
 2. Rename the copy (hereafter refered to as `the style`) to whtever name you whish. This name can be anything, but keeping it within the boundaries of ASCII is probably prefered.
 3. Make changes! Go nuts! The CSS is completely stored in the styles/`the style`/style.css file. You can change this completely to your hearts contents. 
  
And that's really all there is to it. You've got a new style now!  
However, that's not all there is to the styles, and further explanation may be needed, if you want to know what ou're doing.  
It is important to note that these CGI scripts are sourced DIRECTLY by the index.cgi script, and as such, all variables present in the index.cgi script will be available to the templates.  
This includes, but is not limited to, 

 * $styles, the complete physical path to the styles directory.
 * $STYLE, the name of the current style.
 * $path, the complete URI path to the index.cgi file. You can use ${path}/styles/${STYLE}/ to access files from the current style, for external style-specific resources like javascript or css files.
 * $script, the name and full URI of the current script being executed by the shell. This is typically index.cgi. Note that any subshells spawned from index.cgi will not change this variable.
  
