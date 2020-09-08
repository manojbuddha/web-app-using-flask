import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
#############################################################################
############ CONFIGURATIONS (CAN BE SEPARATE CONFIG.PY FILE) ################
#############################################################################

# Remember you need to set your environment variables at the command line
# when you deploy this to a real website.
# export SECRET_KEY=mysecret
# set SECRET_KEY=mysecret
app.config['SECRET_KEY'] = 'mysecret'

#################################
### DATABASE SETUPS ############
###############################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.jinja_env.add_extension('jinja2.ext.loopcontrols')

db = SQLAlchemy(app)
Migrate(app,db)

###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "users.login"



###########################
#### BLUEPRINT CONFIGS #######
#########################


from mywords.users.views import users
from mywords.words.views import words

app.register_blueprint(users)
app.register_blueprint(words)

