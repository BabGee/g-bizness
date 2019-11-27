#How To Run g-bizness

git clone https://github.com/BabGee/g-bizness.git

cd g-bizness

Create your virtual environment and activate it

pip install -r requirements.txt

cd webcommerce

python manage.py migrate

python manage.py runserver