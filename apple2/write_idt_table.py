import numpy as np

anglestring = '0'

g_s_table = np.genfromtxt('D:/Results/UE51/magic_angle/g_s_table_{}.txt'.format(anglestring),skip_header = 1)

a = np.hstack((g_s_table[:,1,None], 3*g_s_table[:,1,None], 5*g_s_table[:,1,None], g_s_table[:,0,None],g_s_table[:,2:]))

print(a)

tabname = 'Ang_{}'.format(anglestring)

idtabmod = 4
idmodesel = 4
lighttype = 4
lighttype_name = tabname
dsets = 3
gapcolumns = 1
shiftcolumns = 1
userdomain_name = ['1st','3rd','5th']
userdomain_comment = tabname
userdomain_units = 'eV'
userdomain_min = [65.0,480.0,800.0]
userdomain_max = [195.0,1560.0,2600.0]
userdomain_slope = [1.0,1.0,1.0]
userdomain_offset = [0.0,0.0,0.0]
monowvlen2energy = 1
auto_interpolation_order = 1

h1_en = np.arange(userdomain_min[0],userdomain_max[0]+1,1)
h3_en = np.arange(userdomain_min[1],userdomain_max[1]+1,1) 
h5_en = np.arange(userdomain_min[2],userdomain_max[2]+1,1)

h1_idx = np.zeros(len(h1_en))
h3_idx = np.zeros(len(h3_en))
h5_idx = np.zeros(len(h5_en))

for i in range(len(h1_en)):
    h1_idx[i] = int(np.where(g_s_table[:,1]==h1_en[i])[0][0])

for i in range(len(h3_en)):
    h3_idx[i] = int(np.where(np.isclose(g_s_table[:,1],h3_en[i]/3,atol = 0.001))[0][0])

for i in range(len(h5_en)):
    h5_idx[i] = int(np.where(np.isclose(g_s_table[:,1],h5_en[i]/5,atol = 0.001))[0][0])

#from e start to e end
#write E
#if E in H0, write H0gap, H0shift
#else write -1

        

with open('D:/Results/UE51/magic_angle/UE51_{}deg_gap_shift.idt'.format(anglestring), 'w') as f:
    f.write('## Data here\n')
    f.write('## Gapfile            = D:/Results/UE51/magic_angle/g_s_table_{}deg.txt\n'.format(anglestring))
    f.write('# Energieshift       =  0.000\n')
    f.write('### Angaben fuer Tkidpreselect_b (Tabellenvorauswahl fuer Andreas Balzer): \n')
    f.write('# IDTBMOD\t{}\n'.format(idtabmod))
    f.write('# IDMODESEL\t{}\n'.format(idmodesel))
    f.write('# LIGHTTYPE\t{}\n'.format(lighttype))
    f.write('# LIGHTTYPE_NAME\t{}\n'.format(lighttype_name))
    f.write('# DATASETS\t{}\n'.format(dsets))
    f.write('# GAPCOLUMNS\t{}\n'.format(gapcolumns))
    f.write('# SHIFTCOLUMNS\t{}\n'.format(shiftcolumns))
    for i in range(3):
        f.write('# USERDOMAIN_NAME[{}]\t{}\n'.format(i,userdomain_name[i]))
        f.write('# USERDOMAIN_COMMENT[{}]\t{}\n'.format(i,userdomain_comment))
        f.write('# USERDOMAIN_UNITS[{}]\t{}\n'.format(i,userdomain_units))
        f.write('# USERDOMAIN_MIN[{}]\t{}\n'.format(i,userdomain_min[i]))
        f.write('# USERDOMAIN_MAX[{}]\t{}\n'.format(i,userdomain_max[i]))
        f.write('# USERDOMAIN_SLOPE[{}]\t{}\n'.format(i,userdomain_slope[i]))
        f.write('# USERDOMAIN_OFFSET[{}]\t{}\n'.format(i,userdomain_offset[i]))
    f.write('# MONOWVLEN2ENERGY\n'.format(monowvlen2energy))
    f.write('# AUTO_INTERPOLATION_ORDER\n'.format(auto_interpolation_order))
    f.write('### Ende der Angaben fuer Tkidpreselect_b.\n')
    
    f.write('##  E [eV]      H1Gap      H1Shift    H3Gap      H3Shift    H5Gap      H5Shift  \n')
    
    for i in range(int(np.min(userdomain_min)),int(1+np.max(userdomain_max))):
        f.write('{:12.5f}'.format(i))
        inh1 = np.where((np.isclose(i,a[:,0],atol = 0.01)))
        if len(inh1[0])==1:
            f.write('{:12.5f}{:12.5f}'.format(a[inh1[0][0],4],a[inh1[0][0],5]))
        else:
            f.write('{:12.5f}{:12.5f}'.format(-1,-1))
        inh3 = np.where((np.isclose(i,a[:,1],atol = 0.01)))
        if len(inh3[0])==1:
            f.write('{:12.5f}{:12.5f}'.format(a[inh3[0][0],4],a[inh3[0][0],5]))
        else:
            f.write('{:12.5f}{:12.5f}'.format(-1,-1))
        inh5 = np.where((np.isclose(i,a[:,2],atol = 0.01)))
        if len(inh5[0])==1:
            f.write('{:12.5f}{:12.5f}\n'.format(a[inh5[0][0],4],a[inh5[0][0],5]))
        else:
            f.write('{:12.5f}{:12.5f}\n'.format(-1,-1))

    
f.close()

print('hey')
    