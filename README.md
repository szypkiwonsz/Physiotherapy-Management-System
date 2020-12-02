# Physiotherapy-Management-System
Project made in Polish language

[**See Project Live Here**](https://fizjo-system.herokuapp.com/)

A web application built in Django that allows you to manage a physiotherapy office. It has many functionalities from the 
side of the office and patient panel, which are described below.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Installing

Clone the repository

```
Open a terminal with the selected path where the project should be cloned
```
```
Type: git clone https://github.com/szypkiwonsz/Physiotherapy_Management_System.git
```

### Prerequisites
Python Version
```
3.8+
```

Libraries and Packages

```
pip install -r requirements.txt
```
---

### Running

A step by step series of examples that tell you how to run a project

(Note: The following command to run celery has been testes only on windows, it requires the gevent package from 
requirements.txt)

```
Download project
```
```
Install requirements
```
```
Run terminal with choosen folder "Physiotherapy_Management_System>" where manage.py file is
```
```
Go to the seetings.py file and at the bottom set the mailbox from which messages will be sent
```
```
Type "python manage.py makemigrations", to make migrations
```
```
Type "python manage.py migrate", to create database
```
```
Set the environment variables as required in the settings.py file
```
```
Run redis server
```
```
Run new terminal with command "celery -A <Physiotherapy_Management_System> worker -l info -P gevent" to start celery
```
```
Type "python manage.py runserver", to start the server
```
---
### Running tests

How to run tests

(Note: ChromeDriver version 80 and Google Chrome version 80 are recommended due to an error that may not run the functional 
tests properly)
```
Do the same as for running the project
```
```
Download the chromedriver.exe from https://chromedriver.chromium.org/downloads/
```
```
Move the downloaded file to "Physiotherapy_Management_System\functional_tests>"
```
```
Open terminal with choosen folder "Physiotherapy_Management_System>" where manage.py file is
```
```
Type: "python manage.py test"
```
---

## Application Features
```
The patient can see the information from the office if the office adds a patient with the same email
```
```
Visibility of registered offices
```
```
Possibility to register as a patient or office
```
```
Sending email asynchronous using celery
```
---

From the patient panel side

```
Arranging visits to registered offices
```
```
Displaying of the medical offices assigned to the patient
```
```
List of future and past visits with the option of editing or canceling them
```
```
Displaying patient medical histories 
```
---

From the office panel side

```
The ability to add patients
```
```
Confirmation of appointments arranged by patients
```
```
Timetable with date selection to add an appointment
```
```
List of visits made by patients in the office
```
```
Adding a medical history for any patient visit
```
---
## Built With

* [Python 3.8](https://www.python.org/) - The programming language used
* [Django 3.0.4](https://www.djangoproject.com/) -  Web framework
* HTML - Hypertext Markup Language
* CSS - Cascading Style Sheet
* [Bootstrap](https://getbootstrap.com/) - HTML, CSS, and JS library
* JavaScript - Scripting language
* [jQuery](https://jquery.com/) - JavaScript library
* AJAX - Set of web development techniques
* [Celery](https://docs.celeryproject.org/en/stable/) - Asynchronous tasks queue
* [Redis](https://redis.io/documentation) - In-memory data structure store
* Unit Tests - Software testing method
* [Selenium](https://www.selenium.dev/) - Automated testing framework

## Authors

* **Jan Kacper Sawicki** - [szypkiwonsz](https://github.com/szypkiwonsz)

## Acknowledgments

* The project was made to better understand the Django framework
