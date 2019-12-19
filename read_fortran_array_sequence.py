#python libraries
import glob
import os
import sys
import argparse

#external libraries
import numpy as np
import scipy as sp

#own libraries
import mat_reader as mr

def get_seedname_list(base_name):
    seedname_list = []
    for infile in sorted(glob.glob(base_name+'*')):
        if infile.endswith('.info'):
                seedname = infile[:-5]
                seedname_list.append(seedname)
    return seedname_list

def read_array_sequence(basename, save_as_numpy_file = True, save_as_text_file=True, find_nonzero_elems=True, threshold = 1e-10):
    #dir_path = "/home/peter/RS_FILES/"
    seedname_list = get_seedname_list(basename)

    for seedname in seedname_list:
        print("reading" + seedname, end = '')
        input_array = mr.read_fortran_array(seedname)
        print ("shape = ", input_array.shape ) 

        if save_as_numpy_file:
            np.save(seedname, input_array)

        if save_as_text_file:
            np.savetxt(seedname+".txt", input_array)
        
        if find_nonzero_elems :
            mr.find_nonzero_elems(seedname, input_array,threshold)

usage = 'read_fortran_array_sequence --basename=basename'

parser = argparse.ArgumentParser( usage, formatter_class=argparse.ArgumentDefaultsHelpFormatter )

parser.add_argument('--basename',
                   action='store',
                   type=str,
                   dest='basename',
                   default=None,
                   help="the relevant files can be found at {target_directory}+/+{basename}+*"\
                    "target_directory defaults to current directory if not set")

parser.add_argument('--target_directory',
                   action='store',
                   type=str,
                   dest='target_directory',
                   default=os.getcwd() + '/',
                   help="the relevant files can be found at {target_directory}+/+{basename}+*")

parser.add_argument('--save_as_npy',
                   action='store',
                   type=bool,
                   dest='save_as_npy',
                   default=True,
                   help="Save matrices as npy files")

parser.add_argument('--save_as_text',
                   action='store',
                   type=bool,
                   dest='save_as_text',
                   default=True,
                   help="Save matrices as human readable text files")

parser.add_argument('--find_nonzero_elems',
                   action='store',
                   type=bool,
                   dest='find_nonzero_elems',
                   default=False,
                   help="find nonzero elements and output values and indexes into text file")

parser.add_argument('--threshold',
                   action='store',
                   type=float,
                   dest='threshold',
                   default=1e-10,
                   help="Threshold for identifying nonzero elements")


args = parser.parse_args(sys.argv[1:])

basename = str(args.target_directory)+str(args.basename)
print("basename = ", basename)
save_as_npy = bool(args.save_as_npy)
save_as_text = bool(args.save_as_text)
find_nonzero_elems = bool(args.find_nonzero_elems)
threshold = np.float64(args.threshold)
read_array_sequence(basename, save_as_npy, save_as_text, find_nonzero_elems, threshold)
