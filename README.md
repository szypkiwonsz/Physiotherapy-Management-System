# Physiotherapy-Management-System
[**See Project Live Here**](https://fizjo-system.herokuapp.com/)

A web application built in Django that allows you to manage a physiotherapy office. It has many functionalities from the side of the office and patient panel, which are described below.

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
Go to the seetings.py file and at the bottom set the mailbox from which messages will be sent.
```
```
Type "python manage.py makemigrations", to make migrations
```
```
Type "python manage.py migrate", to create database
```
```
Type "python manage.py runserver", to start the server
```
---
### Running tests

How to run tests
```
Do the same as for running the project
```
```
Download the [!chromedriver.exe](https://chromedriver.chromium.org/downloads) suitable for your version of Chrome browser
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
The patient can see the information from the office if the office adds a patient with the same email.
```
```
Visibility of registered offices
```
```
Possibility to register as a patient or office
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
* Unit Tests - Software testing method
* [Selenium](https://www.selenium.dev/) - Automated testing framework

## Authors

* **Jan Kacper Sawicki** - [szypkiwonsz](https://github.com/szypkiwonsz)

## Acknowledgments

* The project was made to better understand the Django framework
