# Web D&D (Web-App)

* Created by Dmitry Blotsky and Serghei Filippov on January 9th, 2011

*********************************************************************




# Installation Instructions


1. Clone the repositories
```bash
git clone WEBDND(https://github.com/dblotsky/webdnd)
cd webdnd && git clone SYNCRAE(https://github.com/BlastofWind/syncrae)
```

1. (OPTIONAL) Create a virtualenv
```bash
virtualenv ../webdnd-env
source ../webdnd-env/bin/activate
```

1. Update python packages
```bash
pip install -r shared/config/requirements.txt
```

1. Download and setup the django debug toolbar from: https://github.com/robhudson/django-debug-toolbar
```
cd $(django-debug-toolbar folder)
python setup.py
```

1. Create the local settings file.
```bash
python manage.py localize
vim local_settings.py
```
  * This will create the file from a template
  * Change this file to reflect personal customizations


1. Install http://nodejs.org/
1. Install NPM (which might come with node.js)
1. Setup the precompile scripts
```bash
npm install handlebars -g
npm install less -g
```

