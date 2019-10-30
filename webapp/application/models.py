#all classes defined here which inherit from db.Model map to tables in the sql database
#base classes are defined at the top
from application import db
import numpy as np




class MembraneStructure(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    label=db.Column(db.String(256),index=True,unique=False)
    nPores=db.Column(db.Integer,index=True,unique=False)
    boxSize=db.Column(db.Float,index=True,unique=False)
    lowerC=db.Column(db.Float,index=True,unique=False)
    upperC=db.Column(db.Float,index=True,unique=False)
    poreSizeCeiling=db.Column(db.Float,index=True,unique=False)
    poreSizeFloor=db.Column(db.Float,index=True,unique=False)
    zScaleFactor=db.Column(db.Float,index=True,unique=False)
    def __init__(self, label, nPores, boxSize, lowerC, upperC, poreSizeCeiling, poreSizeFloor,zScaleFactor):
        self.label=label
        self.nPores = nPores
        self.boxSize = boxSize
        self.lowerC = lowerC
        self.upperC = upperC
        self.poreSizeCeiling = poreSizeCeiling
        self.poreSizeFloor = poreSizeFloor
        self.zScaleFactor = zScaleFactor
    def __repr__(self):
        return '<membrane structure %s %s %s %s %s %s %s %s>' % (self.label, self.nPores, self.boxSize, self.lowerC, self.upperC, self.powerSizeCeiling, self.poreSizeFloor, self.zScaleFactor)


class Simulations(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    label=db.Column(db.String(256),index=True,unique=False)
    solute_mesh=db.Column(db.String(256),index=True,unique=False)
    solute_rigid_coords=db.Column(db.String(256),index=True,unique=False)
    solvent_force=db.Column(db.Float,index=True,unique=False)
    solute_solvent_interaction=db.Column(db.Float,index=True,unique=False)
    solute_wall_interaction=db.Column(db.Float,index=True,unique=False)
    n_solutes=db.Column(db.Float,index=True,unique=False)
    steps=db.Column(db.Float,index=True,unique=False)
    status=db.Column(db.String(256),index=True,unique=False)
