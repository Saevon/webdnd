# Web D&D (Web-App)

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

* Create the local settings file.
** This will create the file from a template
** Change this file to reflect personal customizations
```bash
python manage.py localize
vim local_settings.py
```

* Install http://nodejs.org/
* Install NPM (which might come with node.js)
* Setup the precompile scripts
```bash
npm install handlebars -g
npm install less -g
```

