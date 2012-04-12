virtualenv ARCLIB
source ./ARCLIB/bin/activate
pip install -r requirements.txt
python manage.py syncdb
python manage.py loaddata fixtures.json
python runserver 0.0.0.0:1111
