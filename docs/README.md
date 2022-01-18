[![CodeQL](https://github.com/mmpc-nyc/inventory_mgmt/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/mmpc-nyc/inventory_mgmt/actions/workflows/codeql-analysis.yml) [![Django CI](https://github.com/mmpc-nyc/inventory_mgmt/actions/workflows/django.yml/badge.svg)](https://github.com/schir2/inventory_mgmt/actions/workflows/django.yml) ![GitHub commit activity](https://img.shields.io/github/commit-activity/w/mmpc-nyc/inventory_mgmt) ![Size](https://img.shields.io/github/repo-size/schir2/inventory_mgmt) ![GitHub](https://img.shields.io/github/license/schir2/inventory_mgmt)

# Inventory Management for tracking Equipment

## Setup


Create a **.env** in the same location where settings.py resides.
![img.png](img.png)

Run in powershell after creating virtual environment
```powershell
pip install -r requirements.txt
python manage.py setup_initial
```