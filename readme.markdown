*********************************************************************
* README File
* 
* Web DnD Application
* 
* Created by Dmitry Blotsky and Serghei Filippov on January 9th, 2011
*********************************************************************




# Installation Instructions


* Clone the repositories
```bash
git clone WEBDND(https://github.com/dblotsky/webdnd)
cd webdnd && git clone SYNCRAE(https://github.com/BlastofWind/syncrae)
```
* (OPTIONAL) Create a virtualenv
```bash
virtualenv ../webdnd-env
source ../webdnd-env/bin/activate
```
* Update python packages
```bash
pip install -r shared/config/requirements.txt
```
* Adding a local
```bash
python manage.py localize
vim local_settings.py
```
** You can now change this file to reflect personal customizations
* Install http://nodejs.org/
* Install NPM (which might come with node.js)
* Pre-compiler setup
```bash
npm install handlebars
npm install less
```

