# README

The MLTV database project is an open source contribution to the storage and display of projects, as well as information about members and categories in the TV industry.  
This project was started in order to better comform to the Kulturministeriets demand and criteria on how television has to be made. In addition to that, it allows the TV station "Middelfart Lokal TV" ease of use of both the creation of new projects, assignments of responsibilities, as well as editing the projects later.  
  
Currently, the functionality is implemented almost entirely in a single index.cgi script, using only Busybox Ash and SQLite3 (both installed by default in SliTaz) for it's purpose.  
However, a styling and templating system has been implemented, and can be seen in the styles/default directory.  
To create a new style, simply create a new directory in the styles path, and copy the files from styles/default to your new style directory.  
To use the new style, change the variable STYLE in the index.cgi file (in the beginning of the file) to the name of your style directory, no leading or trailing slashes.  
Installation instructions, usage, etc is listed below:
  
 * [Installing](/doc/trunk/doc/install.md)
  
  
For more information you can read the rest of the documentation in the [/doc](/tree?ci=trunk&name=doc) directory.
