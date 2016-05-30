# slimey

##Make sure all files have permission 777. You can do so by running command
sudo chmod -R 777 <directory-name>

##Installation
1. Dependencies can be installed using "install.sh" shell script. Just run ./install.sh from your Linux Terminal.
2. Setup an Xvfb server using shell script "xvfb.sh". @TODO: Run as a backgroud process.
3. Edit your mail server setting in mail.py

##Writing Rules
1. Write your scraping chart in index.py
2. edit your directory-name in nrega.py. TODO: Automatic directory name.

##Running your program
1. Run command "./service.sh" to start the crawler. 

##TODOs
1. URL Monitoring of status.csv and upstart.log
2. API to start script.
3. Master script to control slave servers.
