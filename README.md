# Floodject

This is a master's project created by Ioannis Angelidis, David Nagy and Emil Møller Rasmussen.  

## PyPWS

# Installation structure
The installation directory for the various files roughly looks like this

```
/
└── /usr/
    ├── /local/
    |     ├── /wps/
    |     |   ├── pywps.cfg
    |     |   └── /processes/
    |     |       └── __init__.py
    |     |       └── process1.py
    |     ├── /downloads/
    |         └──  PyWPS-folder
    |
    └── /lib/
        └── /cgi-bin/
            └── pywps.cgi
```

## CGI-BIN

CGI wrapper

```
#!/bin/sh

# Author: Jachym Cepicky
# Purpose: CGI script for wrapping PyWPS script
# Licence: GNU/GPL
# Usage: Put this script to your web server cgi-bin directory, e.g.
# /usr/lib/cgi-bin/ and make it executable (chmod 755 pywps.cgi)

# NOTE: tested on linux/apache

export PYWPS_CFG=/usr/local/wps/pywps.cfg
export PYWPS_PROCESSES=/usr/local/wps/processes/

/usr/local/pywps-VERSION/wps.py $1
```

# Creating functions
It is not the name of the python script, but the name of the "Class" defined within that determines the name of the service.

# GRASS installation on server

```
~
├── .grass7
|     └── rc
└── grassdata
      └── LOCATION
            └── MAPSET

```

# Various URL strings for accessing the WPS service
## Get capabilities
http://54.154.226.176/cgi-bin/pywps.cgi?request=GetCapabilities&service=WPS

## Execute a function
http://54.154.226.176/cgi-bin/pywps.cgi?service=wps&version=1.0.0&request=Execute&identifier=complexRaster&datainputs=[indata=http://54.154.226.176/clip.tif]

## Describe process
http://54.154.226.176/cgi-bin/pywps.cgi?service=wps&version=1.0.0&request=DescribeProcess&identifier=geotiff2png


# Apache2

```
sudo apt-get install apache2
```

Remember to add the server to a security group!

```
sudo a2enmod cgi
```

```
sudo service apache2 restart
```

## File structure of the webserver

```
/
└── /var/
    └── /www/
        └── html
            ├── index.html
            ├── /assets/
            ├── /css/
            ├── / /
            └── /js/
```

## Folders with changes

```
/
└── /etc/
    └── /apache2/
        └── /sites-enabled/
            └── 000-default.conf
```
