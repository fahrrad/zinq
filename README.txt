Hello Free!!!

Om de requirement te downloaden, zou je normaal het volgende moeten doen

1. creeer een virtualenv
 > virtualenv qmenu

2. activeer
 > cd qmenu
 > source bin/activate

Deze stap moet je altijd doen voor je andere commandos kan uitvoeren,
om zeker te zijn dat we dezelfde versies hebben

3. clone git repo > git clone
https://fahrrad@bitbucket.org/fahrrad/qmenu.git

4. install packages >
pip install -r req-dev.txt


Als het niet zou lukken, heb geduld. Ik heb dit nog nooit op een
andere pc gedaan Bel me, of stuur me een mail. We'll figure it out


Django
------

Om de server te starten:

in de qmenu folder ( waar manage.py staat )

1. Om de database te generenen :
 > python manage.py syncdb

2. de embedded webserver starten
 > python manage.py runserver [poort]   
(Standaard is de poort 8000)

Admin interface
---------------

De standaard CRUD schermen zitten onder host:poort/admin. Het paswoord en login is wat
je tijdens 'manage syncdb' hebt opgegeven



