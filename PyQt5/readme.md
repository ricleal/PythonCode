# Ubuntu

In Ubuntu I installed with `apt-get`:

```
python3-pip
libqt5webkit5-dev
python3-pyqt5.qtsvg
python3-pyqt5.qtwebkit
python3-pyqt5.qtopengl
```

`pip3 install plotly`

# In OSX

OSx and Ubuntu have different PyQt versions!!!!

Ubuntu uses `PyQt5.QtWebKitWidgets import QWebView`

Osx uses `PyQt5.QtWebEngineWidgets import QWebEngineView`

`brew install qt5`

`virtualenv -p /usr/local/bin/python3 env`

`pip freeze`

```
appnope==0.1.0
decorator==4.0.10
gnureadline==6.3.3
ipython==4.2.1
ipython-genutils==0.1.0
numpy==1.11.1
pexpect==4.2.0
pickleshare==0.7.2
plotly==1.12.2
ptyprocess==0.5.1
PyQt5==5.6
pytz==2016.4
requests==2.10.0
simplegeneric==0.8.1
sip==4.18
six==1.10.0
traitlets==4.2.2
```
