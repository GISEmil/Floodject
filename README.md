# Floodject

This is a project created by Ioannis Angelidis, David Nagy and Emil Møller Rasmussen.  

## PyPWS

# Installation

Installing PyWPS can be a nightmare if trying to follow the instructions from the official documentation, found below:

```
http://pywps.wald.intevation.org/documentation/installation.html
```

```
http://pywps.wald.intevation.org/documentation/course/
```

One of the developers working on PyWPS gave detailed instructions on how to install PyWPS on Ubuntu 14.04 in the following stackexchange thread:

```
http://gis.stackexchange.com/questions/83743/how-to-install-pywps-on-ubuntu
```

The instructions from there are partly used below, but changed to fit with the individual server setup: 

```
sudo apt-get install apache2 python-setuptools python-magic python-lxml  git-core wget

git clone https://github.com/geopython/PyWPS.git

cd ./PyWPS

sudo python setup.py install
```

```
sudo mkdir /var/www/pywps

sudo mkdir /var/www/wpsoutputs

sudo cp -R pywps/processes /var/www/pywps
```

```
sudo touch /var/www/pywps/pywps.log

sudo cp pywps/default.cfg /var/www/pywps/pywps.cfg

sudo pico /var/www/pywps/pywps.cfg
```

```
  [server]
  maxoperations=30
  maxinputparamlength=1024
  maxfilesize=500mb
  tempPath=/tmp
  processesPath=/var/www/pywps/processes
  outputUrl=http://localhost/wpsoutputs
  outputPath=/var/www/wpsoutputs
  debug=true # deprecated since 3.2, use logLevel instead
  logFile=/var/www/pywps/pywps.log
```

```
sudo chown -R www-data:www-data /var/www/pywps /var/www/wpsoutputs
```

```
sudo cp webservices/cgi/pywps.cgi /usr/lib/cgi-bin

whereis wps.py
```

```
sudo pico /usr/lib/cgi-bin/pywps.cgi
```

```
export PYWPS_CFG=/var/www/pywps/pywps.cfg
export PYWPS_PROCESSES=/var/www/pywps/processes/

/usr/local/bin/wps.py $1
```

```
cd /usr/lib/cgi-bin

sudo sh pywps.cgi "request=GetCapabilities&service=WPS"
```

```
sudo a2enmod cgid
```

```
sudo pico /etc/apache2/sites-available/000-default.conf
```

```
ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/
<Directory "/usr/lib/cgi-bin">
    AllowOverride None
    Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
    Order allow,deny
    Allow from all
</Directory>
```

```
sudo service apache2 restart
```

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
http://52.16.38.28/cgi-bin/pywps.cgi?service=WPS&version=1.0.0&request=getcapabilities

## Execute a function
http://52.16.38.28/cgi-bin/pywps.cgi?service=WPS&version=1.0.0&request=Execute&Identifier=geotiff2png&DataInputs=[input=http://52.16.38.28/clip.tif]

## Describe process
http://52.16.38.28/cgi-bin/pywps.cgi?service=WPS&version=1.0.0&request=DescribeProcess&Identifier=geotiff2png


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
