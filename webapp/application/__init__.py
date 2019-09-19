from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


##every variable "x" initialized in this file is available in the other modules as application.x, and can be imported using "from application import x"

app = Flask(__name__)
#sets all of the configuration variables in the application, see config.py
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)



from application import routes, models
