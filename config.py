import os
basedir= os.path.abspath(os.path.dirname(__file__))

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,
#'bookclub_app.db')
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/bookclub'
WTF_CSRF_ENABLED=True
SECRET_KEY='this-is-a-secret-key'

ADMINS=['example@emailadress.com']
