# FamousHands


## Needed libraries
* pip install cx-Oracle
* pip install djangorestframework
* pip install httplib2
* pip install python-dateutil
* pip install requests
* pip install Wikidata
* pip install wikipedia

## Note regarding cx-Oracle
Current prod deployment is tested with cx-Oracle==5.3

This needs the Oracle Instantclient 12.2 sdk and libs to be installed.

```bash
export LD_RUN_PATH=/opt/oracle/instantclient_12_2
export ORACLE_HOME=/opt/oracle/instantclient_12_2
pip3.4 install cx_Oracle
```

## Note on mod_wsgi
Current prod deployment runs in httpd mod_wsgi
This module needs to be compiled on CentOS 6

Download current release from https://modwsgi.readthedocs.io/en/latest/release-notes/version-4.7.1.html
E.g.:
```bash
wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.7.1.tar.gz
tar -xvf 4.7.1.tar.gz
cd mod_wsgi-4.7.1/
./configure --with-python=/usr/bin/python3.4
make
make install
#make sure /etc/httpd/conf.modules.d/00-wsgi.conf contains the line:
#LoadModule wsgi_module modules/mod_wsgi.so
service httpd configtest
service httpd graceful
```
