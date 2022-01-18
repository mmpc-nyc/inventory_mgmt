[![CodeQL](https://github.com/mmpc-nyc/inventory_mgmt/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/mmpc-nyc/inventory_mgmt/actions/workflows/codeql-analysis.yml) [![Django CI](https://github.com/mmpc-nyc/inventory_mgmt/actions/workflows/django.yml/badge.svg)](https://github.com/schir2/inventory_mgmt/actions/workflows/django.yml) ![GitHub commit activity](https://img.shields.io/github/commit-activity/w/mmpc-nyc/inventory_mgmt) ![Size](https://img.shields.io/github/repo-size/schir2/inventory_mgmt) ![GitHub](https://img.shields.io/github/license/schir2/inventory_mgmt)

# Inventory Management for tracking Equipment

## Setup


Create a **.env** in the same location where settings.py resides.
```dotenv
GOOGLE_API_KEY=GOOGLE_API_KEY # Google API Key Used for geolocation
DEBUG=on #on for debug enabled off for debug disabled
ALLOWED_HOSTS=localhost,127.0.0.1 # your server ip address or hostname
CORS_ALLOWED_HOSTS=http://127.0.0.1:8080,http://localhost:8080 # your frontend base url
```

```powershell
pip install -r requirements.txt
python manage.py setup_initial
```