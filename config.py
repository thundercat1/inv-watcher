SECRET_KEY = 'You will never guess the key'


import os
base_path = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_path, 'app.db')
