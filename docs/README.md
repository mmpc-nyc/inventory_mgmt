[![CodeQL](https://github.com/mmpc-nyc/inventory_mgmt/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/mmpc-nyc/inventory_mgmt/actions/workflows/codeql-analysis.yml) [![Django CI](https://github.com/mmpc-nyc/inventory_mgmt/actions/workflows/django.yml/badge.svg)](https://github.com/schir2/inventory_mgmt/actions/workflows/django.yml) ![GitHub commit activity](https://img.shields.io/github/commit-activity/w/mmpc-nyc/inventory_mgmt) ![Size](https://img.shields.io/github/repo-size/schir2/inventory_mgmt) ![GitHub](https://img.shields.io/github/license/schir2/inventory_mgmt)

# Inventory Management for tracking Equipment

## Setup


Create a **.env** in the same location where settings.py resides.
```yaml
GOOGLE_API_KEY=GOOGLE_API_KEY  			# Google API Key Used for geolocation
DEBUG=on 					# on/off controls debug
ALLOWED_HOSTS=localhost,127.0.0.1 		# django server ip address or hostname
CORS_ALLOWED_HOSTS=http://127.0.0.1:8080	# your frontend base url
```


Run in powershell after creating virtual environment
```powershell
pip install -r requirements.txt
python manage.py setup_initial
```

##Test Running Environment

Django
```shell
python manage.py runserver
```

Vue
```shell
cd frontned/inventory_mgmt
npm run serve
```