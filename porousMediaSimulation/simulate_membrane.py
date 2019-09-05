import argparse
import os, sys
import json
sys.path.insert(0, os.path.abspath('../'))
from porousMediaSimulation.dpdsimulation import DPDSimulation, Statistics 


def save_params(args):
    with open("%s/sim_params.json"%args.output_prefix, "w") as f:
        json.dump(vars(args),f,indent=3)

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='generate a membrane structure from sdf file, and perform a DPD simulation')
    parser.add_argument('--inputfile',dest='membrane_input_file',default='qq.dat',help="sdf membrane structure inputfile")
    parser.add_argument('--output',dest='output_prefix',default='sim_output',help="directory for all of the output files (including membrane geometry, \
        particle trajectories, and stats files and figures)")
    parser.add_argument('--box_size', type=int, dest='box_size',default=50,help="total boxsize for cubic box, default=50")
    parser.add_argument('--composite_solute',dest='composite_solute',action='store_true',default=True,help="include composite solute particles, \
        this does not require an argument, just include --composite_solute to use this")
    parser.add_argument('--solute_mesh',dest='solute_mesh',default="sphere_mesh2.off",help="the .off mesh file containing the solute shape")
    parser.add_argument('--solute_rigid_coords',dest='solute_rigid_coords',default="rigid_coords.txt",help="the .txt file containing the coordinates of particles in a single solute molecule")
    parser.add_argument('--solvent_radius',type=float,dest='solvent_radius',default=1.0,help="size of the solvent particles, default=1.0")
    #parser.add_argument('--solute_radius',type=float,dest='solute_radius', default=0.0, help="size of the solute particles, default=0.0, which corresponds to no solute")
    parser.add_argument('--solvent_density',type=float, dest='solvent_density', default=5, help="density of the solvent, default=5")
    #parser.add_argument('--solute_density',type=float, dest='solute_density', default=0.1, help="density of the solute, default=0.1")
    parser.add_argument('--solvent_force', type=float, dest='solvent_force', default=-0.1, help="force acting on the solvent particles pushing them through the membrane, default=-0.1")
    #parser.add_argument('--solute_force', type=float, dest='solute_force', default=0.1, help="force acting on the solute particles pushing the through the membrane, default=0.1")
    parser.add_argument('--solute_solvent_interaction',type=float,dest='solute_solvent_interaction', default=35, help="strength of solute solvent interaction, >35 means hydrophobic, default=35 (neutral)")
    parser.add_argument('--solute_wall_interaction',type=float,dest='solute_wall_interaction', default=45, help="strength of solute membrane interaction, <35 means attractive, default=35")
    parser.add_argument('--dump_every',type=int,dest='dump_every', default=1500, help="number of steps between writing snapshots of the particles, default is 1500")
    parser.add_argument('--steps',type=int, dest='steps', default=100000, help="number of simulation steps, default is 100000")
    parser.add_argument('--membrane_lower_boundary', type=float, dest='membrane_lower_boundary', default=15, help="the lower boundary of the membrane, this is used to compute flow rate, default=15")
    parser.add_argument('--solute_z_position', type=float, dest='solute_z_position', default=45, help="the initial z position of the solutes, default=45")
    parser.add_argument('--sqrt_n_solutes', type=int, dest='sqrt_n_solutes', default=4, help="the square root of the number of solute particles, default=4")
    args=parser.parse_args()
    os.system("mkdir %s"%args.output_prefix)
    save_params(args)
    #check that box size from input and box size from sdf file are the same
    with open(args.membrane_input_file.split('.')[0]) as f:
        box_size_from_file = int(f.readline().split(' ')[0])
    if box_size_from_file != args.box_size:
        raise RuntimeError("box size provided does not match box size in input file, input file says box size is %d"%box_size_from_file)

    simulation=DPDSimulation(membrane_input_file=args.membrane_input_file,output_prefix=args.output_prefix,\
        box_size=args.box_size,composite_solute=args.composite_solute)
    #simulation.initializeSolute(density=args.solute_density,radius=args.solute_radius,force=args.solute_force)
    simulation.initializeSolvent(density=args.solvent_density,radius=args.solvent_radius,force=args.solvent_force)
    if args.composite_solute:
        simulation.initializeRigidSolute(a=args.solute_solvent_interaction, z_position=args.solute_z_position, \
            num_particles_sqroot=args.sqrt_n_solutes, mesh_file=args.solute_mesh, coord_file=args.solute_rigid_coords)
    simulation.initializeWall(solute_interaction_strength=args.solute_wall_interaction)
    simulation.createOutput(dump_every=args.dump_every)
    #initialize the simulations statistics object
    simulation.statistics()

    simulation.runSimulation(steps=args.steps,stats_every=1000)
