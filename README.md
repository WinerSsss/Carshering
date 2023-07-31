# TAKE&DRIVE
Car renting service

This is an application which allows users to rent or list personal car.

## 1. Getting started
1.1 To run this application you need to have installed Python. If you don't have it already, please visit 
    Python.org to download it.


1.2 Download 

   - You need to clone repository to your local destination

           $ cd path/to/your/workspace

           git clone https://github.com/WinerSsss/Carshering

1.3 Requirements
   - Once your virtual environment is activated and project is cloned you need to install requirements:

           pip install -r requirements.txt

1.4 Database
   - This application uses SQLite database. To create database you need to type:

           python manage.py makemigrations carservice
           python manage.py makemigrations users
           python manage.py migrate carservice
           python manage.py migrate users
           python manage.py makemigrations
           python manage.py migrate

1.5 Configuration
   - Create a .env file in the root directory of the project.
   - In the .env file, add the following lines:

           SECRET_KEY="your_secret_key"
           DEBUG=True

     Replace "your_secret_key" with your desired secret key value.

## 2. Usage
2.1 To use this application you need to type (if you're in your workspace directory):

        python manage.py runserver
    or 

        python3 manage.py runserver

2.2 After that you need to create an account to start using app.


2.3 Main functionalities:
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
  - Generating PDF reports with rent information


2.4 To do:
  - Adding localization
  - Adding map home page
  - Adding cars/offers sorting


2.5 Technologies used:
  - crispy-bootstrap5==0.7
  - Django==4.2.2
  - django-crispy-forms==2.0
  - pytest==7.4.0
  - pytest-cov==4.1.0
  - pytest-django==4.5.2
  - python-dotenv==1.0.0
  - Docker
  - Travis CI

## 3. Running in Docker container

To run the application in a Docker container, follow these steps:

3.1. Build the Docker image:

```docker build -t takedrive .```

3.2. Run the Docker container:

```docker run -p 8001:8001 takedrive```

After executing these steps, the application will be available at http://localhost:8001/.

Note: Make sure you have Docker installed on your computer before attempting to run in a container.

## 4. Running Tests

To run the tests, execute the following command:
```pytest --ds=Carshering.settings```git check

## 5. Screenshots

![Opis obrazka](https://i.gyazo.com/d19af5906775075deb9200fa79fe5e43.png)
![Opis obrazka](https://i.gyazo.com/0de0497039092b52529439c41589db64.png)
![Opis obrazka](https://i.gyazo.com/1d6e322eae20b73f6c5e43892157dd0f.png)
![Opis obrazka](https://i.gyazo.com/00d3a2a4181c6e1a813eb5c2a25b0edf.png)
![Opis obrazka](https://i.gyazo.com/bbe55dbe1b01148ca268e0ab4532a2ca.png)
![Opis obrazka](https://i.gyazo.com/89c200d5ad3c2dcd5ee6be888fbf04a5.png)
