To start the webstore, tpe the following two commands when you are in the 2/ folder:

docker build -t butikk .

docker run -p 5001:5001 butikk 

This project is a bit frankensteined. In the Dockerfile the requirements are installed and port 5001 is exposed.
In the app folder the python files can be found and the templates folder, which are the most important files.

 In the templates folder are all the html files used. 

 In the python files are the python code for the project. There is a config file with configuration, a init file that, well, initalizes. 
 
 The forms file is for the forms mnodule.

 The models file is for the databse.

 The routes file includes all the routes.

 The utils file is used for Two factor.

 THe imports are kind of a mess, mostly cause I didn't really have a clear idea when starting out.