# Woodkirk Valley FC
Woodkirk Valley FC Skills Matrix Website

Website developed to develop players skills and gain badges


Install Instructions:

* Setup python with Virtual Environment
* Install requirements.txt
* runserver


# Useful Commands
```
# Migrations
python manage.py makemigrations member
python manage.py migrate member

# fake migration if out of sync
python manage.py migrate member --fake

## Dump Export and Import from Database as JSON
python manage.py dumpdata > export28052017.json
python manage.py loaddata export28052017.json
```