# TAKE&DRIVE
Car renting service

This is an application which allows users to rent or list personal car.

## Getting started
1. To run this application you need to have installed Python. If you don't have it already, please visit 
    Python.org to download it.


2. Download 

   - You need to clone repository to your local destination

           $ cd path/to/your/workspace

           git clone https://github.com/WinerSsss/Carshering

3. Requirements
   - Once your virtual environment is activated and project is cloned you need to install requirements:

           pip install -r requirements.txt

4. Database
   - This application uses SQLite database. To create database you need to type:

           python manage.py makemigrations carservice
           python manage.py makemigrations users
           python manage.py migrate carservice
           python manage.py migrate users

## Usage
- To use this application you need to type (if you're in your workspace directory):

        python manage.py runserver
    or 

        python3 manage.py runserver

- After that you need to create an account to start using app.


- Main functionalities:
  - Add car to rent with all details
  - List cars in offer tab
  - Rent car
  - Add car to rent
  - Choose rent timeline
  - Update offer
  - Update car details
  - User registration/login
  - Updating user profile
  - Password change
  - Rent panel with history of rents


- To do:
  - Adding localization
  - Adding map home page
  - Adding cars/offers sorting


5. Technologies used:
  - crispy-bootstrap5==0.7
  - Django==4.2.2
  - django-crispy-forms==2.0
  - pytest==7.4.0
  - pytest-cov==4.1.0
  - pytest-django==4.5.2
  - python-dotenv==1.0.0
