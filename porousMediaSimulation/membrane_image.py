import argparse
import os, sys
sys.path.insert(0, os.path.abspath('../'))
from porousMediaSimulation.dpdsimulation import DPDSimulation 


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='')
    parser.add_argument('--inputfile',dest='membrane_input_file',default='qq.dat',help="sdf membrane structure inputfile")
    parser.add_argument('--output',dest='output_prefix',default='membrane/wall',help="prefix for the output h5 and xmf file of the membrane")
    parser.add_argument('--box_size', type=int, dest='box_size',default=50,help="total boxsize for cubic box, default=50")
    args=parser.parse_args()

    with open(args.membrane_input_file.split('.')[0]) as f:
        box_size_from_file = int(f.readline().split(' ')[0])
    if box_size_from_file != args.box_size:
        raise RuntimeError("box size provided does not match box size in input file, input file says box size is %d"%box_size_from_file)

    simulation=DPDSimulation(membrane_input_file=args.membrane_input_file,output_prefix=args.output_prefix, \
                             box_size=args.box_size)
    simulation.drawWall()
