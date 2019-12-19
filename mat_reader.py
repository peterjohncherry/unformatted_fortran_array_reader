import sys
import os
import numpy as np
from scipy.io import FortranFile

def read_binary_fortran_file(name, datatype, dim0, dim1=1 ):

    input_array=np.ndarray((dim0*dim1))

    if dim1 == 1 :
        fmat = FortranFile(name, 'r')
        if (datatype == "real"):
            input_array = fmat.read_reals(dtype=np.float64)
        if (datatype == "int"):
            input_array = fmat.read_ints(dtype=np.int32)
    
        print( name+"shape = " , input_array.shape)
        fmat.close()

    else :
      if (datatype == "real"):
          fmat = FortranFile(name, 'r')
          input_array = fmat.read_reals(dtype=np.float64)
          input_array = input_array.reshape((dim0,dim1)).transpose()
          fmat.close()

      elif (datatype == "int"):
          fmat = FortranFile(name, 'r')
          input_array = fmat.read_ints(dtype=np.int32)
          input_array = input_array.reshape((dim0,dim1)).transpose()
          fmat.close()

      elif ( datatype == "complex" ):
          sys.exit("reading of complex matrices is not directly possible, must write out real and imag parts " \
                   "as two seperate real matrices\n")

      else :
          sys.exit("reading of datatype \"" +  datatype + "\" is not implemented\n ")

    return input_array

#reads the matrix info file which is generated to aid reading of fortran binary file
def read_array_info_file(name):

    infofile = open(name,"r")
    for line in infofile.readlines():
        line_array = line.split()
        if line_array[0] == "dim0":
            dim0 = int(line_array[2])
        elif line_array[0] == "dim1":
            dim1 = int(line_array[2])
        elif line_array[0] == "datatype":
            datatype = str(line_array[2])

    return dim0, dim1, datatype

def read_fortran_array(seedname):
    nrows, ncols, datatype = read_array_info_file(seedname+".info")

    if datatype == "complex" :
        name =seedname+"_real.bin"
        array_real =  read_binary_fortran_file(name, "real", nrows, ncols)
        name = seedname+"_imag.bin"
        array_imag = read_binary_fortran_file( name, "real", nrows, ncols)
        return array_real + 1j*array_imag

    elif datatype == "real" :
        name = seedname+".bin"
        array_real =  read_binary_fortran_file(name, datatype, nrows, ncols)
        return array_real

    elif datatype == "int" :
        name =seedname+".bin"
        array_ints =  read_binary_fortran_file(name, datatype, nrows, ncols)
        return array_ints

    else :
        sys.exit("Not implemented " + datatype + " ABORTING" )

def find_nonzero_elems(seedname, input_array, threshold = 1e-10):
    non_zero_ids = np.argwhere(np.abs(input_array) > threshold )

    non_zero_elems = []
    for idx in non_zero_ids : 
        non_zero_elems.append(input_array[idx])

#    np.savetxt(seedname+"_nonzero_ids.txt", non_zero_ids, fmt ='%.4i')
#    np.savetxt(seedname+"_nonzero_elems.txt", non_zero_elems)
    outfile = open (seedname+"_nonzero.txt","w+" )
    for ii in range(len(non_zero_ids)):
        outfile.write(str(non_zero_ids[ii]) + " = " + str(non_zero_elems[ii]) +"\n" )

    outfile.close()
        
 
    
def read_numpy_array(name):
    return np.load(name)
