from functools import wraps
import json
import numbers
import ast
import os
import time
import math
import csv
import numpy as np
import datetime
import socket
import codecs
import ssl
import threading
import scipy.io
import itertools
import pickle

from flask import Flask,render_template,request,redirect,jsonify,send_file,session,flash, url_for, g, Response, copy_current_request_context
#from webui import WebUI
#from pyfladesk import init_gui
from flask_session import Session
from application import db
from application import app

from application.models import *
from application.forms import *
import sys
sys.path.append('..')
from porousMediaSimulation.pore_network_sdf import PoreNetwork

from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Category10


#import pandas as pd

from io import StringIO
#import paho.mqtt.client as paho
from bokeh.models.sources import AjaxDataSource, ColumnDataSource


from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


sess=Session()
sess.init_app(app)

app.vars={}





@app.route('/home',methods=['GET','POST'])
@app.route('/',methods=['GET','POST'])
def index():
    session['username']='user1'
    return render_template('index.html')



@app.route('/structures', methods=['GET', 'POST'])
def structures():
    form=StructuresForm()
    structures=MembraneStructure.query.order_by(MembraneStructure.id.desc()).limit(20).all()
    if form.validate_on_submit():
        pn=PoreNetwork(npores=form.npores.data,boxsize=form.boxSize.data,lowerc=form.lowerC.data,upperc=form.upperC.data,poresizeceiling=form.poreSizeCeiling.data,poresizefloor=form.poreSizeFloor.data,outputpath=form.label.data)
        pn.QQ_parallel()
        pn.generate_h5()
        pn.generate_image()
        structure=MembraneStructure(label=form.label.data,nPores=form.npores.data,boxSize=form.boxSize.data,lowerC=form.lowerC.data,upperC=form.upperC.data,poreSizeCeiling=form.poreSizeCeiling.data,poreSizeFloor=form.poreSizeFloor.data)
        db.session.add(structure)
        db.session.commit()
        structures=MembraneStructure.query.order_by(MemraneStructure.id.desc()).limit(20).all()
        return render_template('structures.html',structures=structures, form=form)

    return render_template('structures.html',structures=structures, form=form)
