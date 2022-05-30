'''
Created on 18 Jan 2022

@author: oqb
'''

import numpy as np

if __name__ == '__main__':
    dirpath = 'M:/Python/idt/idt/'
    fname = 'Ang00p_h135.idt'
    print(fname)
    bigfname = 'M:/Python/idt/idt/ba_file.idt'
    a = np.genfromtxt('{}{}'.format(dirpath,fname))
    
    try:
        with open(bigfname) as file:
            f = open(bigfname, 'a')
        # do whatever
    except IOError:
        f = open(bigfname, 'a')
        f.write('#Gap       \tShift     \tEnergy    \tPhase     \tHarmonic\n')
    # generate the file

    #check if file exists
    #create it if it doesn't exist
    
    if fname[5] == 'p':
        phase = int(fname[3:5])
    else:
        phase = -1 * int(fname[3:5])
    
    #open file
    #for harmonic in range 3
    for line in range(len(a)):
        for i in range(3):
            gap = a[line, 2*i+1]
            shift = a[line, 2*i+2]
            energy = a[line,0]
            n = 2*i+1
            if gap > 0:
                newline = '{:10.4f}\t{:10.4f}\t{:10.1f}\t{:10.1f}\t{:10.0f}\n'.format(gap, shift, energy, phase, n)
                f.write(newline)
            #append
    
    angle = ['10','15','20','30','40','45','50','60','70','75','80','90']
    polarisation = ['n','p']
    
    for aa in angle:
        for pp in polarisation:
            fname = 'Ang{}{}_h135.idt'.format(aa,pp)
            print(fname)
            if fname[5] == 'p':
                phase = int(fname[3:5])
            else:
                phase = -1 * int(fname[3:5])
                
            a = np.genfromtxt('{}{}'.format(dirpath,fname))
            for line in range(len(a)):
                for i in range(3):
                    gap = a[line, 2*i+1]
                    shift = a[line, 2*i+2]
                    energy = a[line,0]
                    n = 2*i+1
                    if gap > 0:
                        newline = '{:10.4f}\t{:10.4f}\t{:10.1f}\t{:10.1f}\t{:10.0f}\n'.format(gap, shift, energy, phase, n)
                        f.write(newline)
    
    print(1)