import numpy as np
import math
import sys, os
import json
import argparse
import multiprocessing


class PoreNetwork(object):
    def __init__(self,npores,boxsize,zboxsize,lowerc,upperc,pore_radius,outputpath):
        self.npores=npores
        self.boxsize=boxsize
        self.zboxsize=zboxsize
        self.lowerc=lowerc
        self.upperc=upperc
        self.pore_radius=pore_radius
        self.q=self.createGrid()
        self.gridpores=self.createGridPores()
        self.throats=self.createThroats()
        self.outputpath=outputpath

    def poresize(self,pore):
        psize=self.pore_radius+(self.pore_radius+3.0-self.pore_radius)*(pore[2]-float(self.lowerc))/float(self.upperc-self.lowerc)
        #return self.pore_radius
        return psize
    
    def distance(self,p1,p2):
        return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2)

    def norm(self,p1):
        return p1[0]**2+p1[1]**2+p1[2]**2

    def createGrid(self):
        x=np.arange(0,self.boxsize,2.0,dtype=np.float32)
        y=np.arange(0,self.boxsize,2.0,dtype=np.float32)
        z=np.arange(0,self.zboxsize,2.0,dtype=np.float32)
        q=np.vstack(np.meshgrid(x,y,z,indexing='ij')).reshape(3,-1).T #array of 3d numbers
        return q

    def createPores(self):
        x=np.random.uniform(0,self.boxsize,self.npores)
        y=np.random.uniform(0,self.boxsize,self.npores)
        z=np.random.uniform(self.lowerc+5,self.upperc,self.npores)
        pores=np.vstack([x,y,z]).T
        return pores

    def createGridPores(self):
        spacing=(self.boxsize)/np.sqrt(self.npores)
        xy=np.arange(8,self.boxsize-4,int(spacing))
        if self.npores==1:
            xy=np.arange(self.boxsize/2,self.boxsize/2+1)
        gridpores=[]

        for x in xy:
            for y in xy:
                gridpores.append([x,y,self.lowerc])
                gridpores.append([x,y,self.upperc])
        return np.asarray(gridpores)

    def createThroats(self):
        throats=[]
        for i in range(0, len(self.gridpores),2):
            throats.append([i,i+1])
        self.pores=np.vstack([self.gridpores])
        return throats

    def inthroat(self,node1,node2,x):
        throatlength=self.distance(node1,node2)
        distanceFromLine=math.sqrt((self.norm(x-node1)*self.norm(node1-node2)-np.dot(node1-x,node2-node1)**2)/(self.norm(node2-node1)))
        midpoint=0.5*(node1+node2)
        distanceFromMidpoint=self.distance(x,midpoint)
        parallelDistance=math.sqrt(distanceFromMidpoint**2-distanceFromLine**2)
        ps1=self.poresize(node1)
        ps2=self.poresize(node2)
        d1=self.distance(x,node1)
        d2=self.distance(x,node2)
        dp=0
        if d1 >d2:
            dp=distanceFromMidpoint+throatlength/2
        else:
            dp=throatlength/2-distanceFromMidpoint
        adjustedporesize=ps1+dp*(ps2-ps1)/throatlength
        if distanceFromLine<adjustedporesize and parallelDistance < (throatlength/2):
            return True
        else:
            return False

    def inpores(self,x):
        for pore in self.pores:
            if self.distance(x,pore) < self.poresize(pore):
                return True
        return False

    def inthroats(self,x):
        for throat in self.throats:
            if self.inthroat(self.pores[throat[0]],self.pores[throat[1]],x):
                return True
        return False

    def sdf(self,x):
        if (x[2]>self.upperc or x[2]<self.lowerc):
            return -0.5
        elif (x[0]>(self.boxsize-3) or x[0]<3 or x[1]>(self.boxsize-3) or x[1]<3):
            return 0.5
        elif self.inpores(x):
            return -0.5
        elif self.inthroats(x):
            return -0.5
        else:
            return 0.5

    def QQ(self):
        self.qq=[self.sdf(x) for x in self.q] #sdf values
        return None

    def QQ_parallel(self):
        p=multiprocessing.Pool()
        self.qq=p.map(self.sdf,self.q)
        return None

    def output(self):
        qnp=np.asarray(self.qq,dtype=np.float32)
        outputfile="%s/qq.dat"%self.outputpath
        tempfile="%s/q.dat"%self.outputpath
        qnp.tofile(tempfile)
        sizefile="%s/qq"%self.outputpath
        #sizefile=outputfile.split('.')[0]
        with open(sizefile,"w") as f:
            f.write("%d %d %d\n"%(self.zboxsize,self.boxsize,self.boxsize))
            f.write("%d %d %d\n"%(self.zboxsize/2,self.boxsize/2,self.boxsize/2))
        os.system("cat %s %s >%s"%(sizefile,tempfile,outputfile))

    def generate_h5(self):
        sys.path.insert(0, os.path.abspath('../'))
        from porousMediaSimulation.dpdsimulation import DPDSimulation
        outputfile="%s/qq.dat"%self.outputpath
        print("hi")
        simulation=DPDSimulation(membrane_input_file=outputfile,label=self.outputpath, \
                                 box_size=self.boxsize,z_box_size=self.zboxsize, ranks=1)
        simulation.drawWall()
        print("wall generated")

    def generate_image(self):
        os.system("/usr/local/visit/bin/visit -cli -nowin -s /home/shafferpr/membrane_simulations/porousMediaSimulation/visit_script.py %s/wall.xmf"%self.outputpath)
        os.system("mv visit0000.png %s/."%self.outputpath)

def save_params(args):
    with open("%s/membrane_params.json"%args.outputpath, "w") as f:
        json.dump(vars(args),f,indent=3)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='create a membrane structure')
    parser.add_argument('--npores', type=int, dest='npores',default=12,help="number of cylindrical pores in the membrane")
    parser.add_argument('--boxsize', type=int, dest='boxsize',default=50,help="total boxsize for cubic box, default=50")
    parser.add_argument('--zboxsize', type=int, dest='zboxsize',default=50,help="z box dimension, default=50")
    parser.add_argument('--lowerc', type=int, dest='lowerc',default=15,help="lower cutoff for the membrane structure in the box, default=15")
    parser.add_argument('--upperc', type=int, dest='upperc',default=35,help="upper cutoff for the membrane structure in the box, default=35")
    parser.add_argument('--pore_radius', type=float, dest='pore_radius',default=6,help="pore radius, default=6")
    parser.add_argument('--outputpath',dest='outputpath',default='membrane',help="output directory, used as input to simulation, default=membrane")
    parser.add_argument('--runparallel',dest='runparallel',action='store_true',default=False,help="run multiple threads in parallel, this does not require an argument, just include --runparallel to use this")
    parser.add_argument('--create_image',dest='create_image',action='store_true',default=False,help="create a png image of the membrane using visit")
    args = parser.parse_args()
    os.system("mkdir %s"%args.outputpath)
    save_params(args)
    pn=PoreNetwork(npores=args.npores,boxsize=args.boxsize,zboxsize=args.zboxsize,lowerc=args.lowerc,upperc=args.upperc,pore_radius=args.pore_radius,outputpath=args.outputpath)
    if args.runparallel:
        pn.QQ_parallel()
    else:
        pn.QQ()
    pn.output()
    print("generating image")
    pn.generate_h5()
    if args.create_image:
        pn.generate_h5()
        pn.generate_image()
