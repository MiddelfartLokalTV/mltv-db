# Installation

Thankfully the MLTV database backend system is easy to install, and there are no strange installation steps.  
However, there are a few things to keep in mind. Since this project makes use of the httphelper script from SliTaz, that script or a SliTaz RC5.0-RC2 (or newer) installation is prefered.  
Now, the dependencies are as follows:  

 * A mod_cgi compatible HTTP server (Busybox HTTP can work, lighttpd prefered)
 * SQLite3 installation (preinstalled on SliTaz)
 * A POSIX compliant shell (Busybox Ash works, however bash, and dash can also be used)

Now, those are the dependencies, and with that out of the way, here's the installation instructions:

 1. Download this repository. You can do so for instance by going to [this link](/download).
 2. Move the entire repository directory to the web directory. On SliTaz this is typically /var/www.
 3. There is no step 3. You are already done.
  
