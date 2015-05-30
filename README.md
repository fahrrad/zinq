App to take orders from tables in cafe/ restaurants

See wiki for more info on how to start the project

* voor installatie in Macos X Maverick
Nodig voor het compileren van psyocpg2 en pil

export CPPFLAGS=-Qunused-argument
export CFLAGS=-Qunused-arguments

* Error on macosX

* DONE make all links to webresources (like jquery availble) ofline

running on macosX
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

running against the heroku settings
export DJANGO_SETTINGS_MODULE=settings_heroku

user stories
------------

Implemented 
-----------

When as a consumer, I scan a QR code on a table, I want to see the menu for the place with all the categories collapsed.

When, as a consumer, I'm looking at the menu, I click on a collapsed catergory, I want to see the items on the menu in 
that category

When, as a consumer, I'm looking at the menu, and click on the button labelled with a '+' I want to see the count of
that item increase. Also, the total count should increase with one. 

When, as a consumer, I'