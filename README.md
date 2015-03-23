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

## Actual installation

Install dependencies, clone the project from GitHub and install it:

```
sudo apt-get install apache2 python-setuptools python-magic python-lxml  git-core wget

git clone https://github.com/geopython/PyWPS.git

cd ./PyWPS

sudo python setup.py install
```

## Create folders for PyWPS assets

For convenience, in this example all PyWPS assets are stored in /var/www/html, a typical setup for a development environment. In a server setup it might be wiser to store processes in /srv and logs in /var/log.

```
sudo mkdir /var/www/html/pywps

sudo mkdir /var/www/html/wpsoutputs

sudo cp -R pywps/processes /var/www/html/pywps
```

Create log and configuration files:

```
sudo touch /var/www/html/pywps/pywps.log

sudo cp pywps/default.cfg /var/www/html/pywps/pywps.cfg

sudo pico /var/www/html/pywps/pywps.cfg
```

In the configuration file only the Server environment needs to be tweaked, in order to match the asset locations created before. The set up of the GRASS and MapServer environments are left for a later date.

```
  [server]
  maxoperations=30
  maxinputparamlength=1024
  maxfilesize=500mb
  tempPath=/tmp
  processesPath=/var/www/html/pywps/processes
  outputUrl=http://localhost/wpsoutputs
  outputPath=/var/www/html/wpsoutputs
  debug=true # deprecated since 3.2, use logLevel instead
  logFile=/var/www/pywps/pywps.log
```

Pass ownership to the www-data user (again, in a server setup you might want to be more conservative):

```
sudo chown -R www-data:www-data /var/www/html/pywps /var/www/html/wpsoutputs
```

## Configure the web service

Copy the PyWPS CGI to /usr/lib/cgi-bin:

```
sudo cp webservices/cgi/pywps.cgi /usr/lib/cgi-bin

whereis wps.py
```

Copy the path of wps.py to the clipboard.

```
sudo pico /usr/lib/cgi-bin/pywps.cgi
```

Modify pywps.cgi to match the present setup:

```
export PYWPS_CFG=/var/www/pywps/html/pywps.cfg
export PYWPS_PROCESSES=/var/www/pywps/html/processes/

/usr/local/bin/wps.py $1
```

Give it a try:

```
cd /usr/lib/cgi-bin

sudo sh pywps.cgi "request=GetCapabilities&service=WPS"
```

Make sure Apache is configured to run CGI scripts; the CGI module might need to be explicitly enabled:

```
sudo a2enmod cgid
```

Edit the default site configuration

```
sudo pico /etc/apache2/sites-available/000-default.conf
```

Verify that this section is included, add the necessary keywords to make it look like this (in Ubuntu 12.04 this may already be the default configuration):

```
ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/
<Directory "/usr/lib/cgi-bin">
    AllowOverride None
    Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
    Order allow,deny
    Allow from all
</Directory>
```

Restart Apache:

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
