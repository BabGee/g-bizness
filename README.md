## Hosted 

https://loxpack.pythonanywhere.com/

## Screenshots

![gcart](https://user-images.githubusercontent.com/39271713/75942524-a3dbe980-5ea3-11ea-8f4b-a154fb18f43d.png)

![chkt](https://user-images.githubusercontent.com/39271713/75101250-6b5a2700-55ea-11ea-9bac-9c7dcfcc7dd4.png)


# g-bizness

**g-bizness** is a E-commerce system written in Python 3 and using Django framework.
The application allows users add to cart products and checkout. It allows admins to add different Categories and products in the backend. 


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See installing instructions for notes on how to deploy the project on a live system.


### In development features

* Payment intergration

### Installation

Get a local copy of the project directory by cloning "smart-parking-management" from github.

```bash
git clone https://github.com/BabGee/g-bizness.git
```

cd into the folder

```bash
cd g-bizness
```

The Framework, Packages and Libraries used in this project are installed in a virtual environment(Recommended); i use pipenv. Instructions on how to get pipenv [here](https://pypi.org/project/pipenv/)

```bash
python3 -m pipenv shell
```

Install the requirements

```bash
python3 -m pip install -r requirements.txt
```

Then follow these steps:
1. Move to root folder 

```bash
cd webcommerce
```

2. Create the tables with the django command line

```bash
python3 manage.py makemigrations
```
then migrate the changes
 
```bash
python3 manage.py migrate
```

Create an admin using command below and enter your preferred username, email and password.(You will use this to create products that user will view)
 
```bash
python3 manage.py createsuperuser
```


3. Finally, run the django server

```bash
python manage.py runserver
```

4. Access the django admin by adding ' /admin' to the url and login to products.



## Built With

* [Python 3](https://www.python.org/downloads/) - Programming language
* [Django](https://www.djangoproject.com/) - Web framework 


## Versioning
I use exclusively Github

## License

This is an open source project not under any particular license.
However framework, packages and libraries used are on their own licenses. Be aware of this if you intend to use part of this project for your own project.

