"""This module sets up the application variables"""
# imports the application and the database
from application import app, db
from application.models import *
#from waitress import serve #use this when running in production
# from pyfladesk import init_gui

@app.shell_context_processor
def make_shell_context():
    """These lines configure some variables for use when using "flask shell"""
    return {"db": db}


# if the command python nirrin_app.py is used to run the app,
# the lines of code beneath here are executed.
# if flask run is used to run the app, I believe application.run()
# is executed automatically in some way

if __name__ == '__main__':
    # db.init_app(application)

    # application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    # db.init_app(application)
    # sess.init_app(application)
    # application.run(host='0.0.0.0')
    app.run(host='0.0.0.0',port=443,ssl_context='adhoc')
    #app.run(host='0.0.0.0',port=80)
    #serve(app,host='0.0.0.0',port=8080) #use this when running in production
# ui.run()  ##use this line when running as a desktop app
# init_gui(application)
