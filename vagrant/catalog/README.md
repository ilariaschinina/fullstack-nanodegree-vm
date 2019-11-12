# Catalog App for a small coding book collection
This app has been built as project for the Udacity Full Stack Web Developer Nanodegree program.
It is a small catalog app that organizes books for learning programming languages.

Main features:
* The basic CRUD functionalities have been implemented and only the authorized users can have access to them
* The app supports OAuth2 login with Google
* The project implements JSON endpoints that serve the same information as displayed in the HTML endpoints:
    * for arbitrary item in the catalog
    * for all categories
    * for a single category

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Prerequisites: VM](#prerequisites-VM)
- [Prerequisites: the data](#prerequisites-the-data)
- [Running](#running)


### Prerequisites: VM

* Install [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
* Install [Vagrant](https://www.vagrantup.com/downloads.html)
	* Run `vagrant --version` to be sure that Vagrant is successfully installed)
* The VM configuration is included in this repository
* Start the virtual machine from your terminal while being inside the **vagrant** subdirectory by running:
	* `vagrant up`
	* `vagrant ssh`
* Now you are logged, change directory with `cd /vagrant/catalog`. Files in the VM's `/vagrant` directory are shared with the vagrant folder on your computer

### Prerequisites: the data

* Run `pip3  install  -r  requirements.txt` in order to install the dependencies
* Run `python3 db_setup.py`to generate the database
* Run  `python3 db_data.py` to populate the database
* Create a [Google credential file](https://console.cloud.google.com/projectselector2/home/dashboard) (to allow Google login), name it `client_secret.json` and place in the `catalog` folder

### Running

* Before launching the main script, type in your terminal `export OAUTHLIB_INSECURE_TRANSPORT=1` (this is to avoid having to use https with Oauthlib)
* Run now `python3 application.py`
* Open your browser and go to `http://localhost:5000`
