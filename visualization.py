import matplotlib.pyplot as plt
from easyVasp.dosfile import Doscar
import numpy as np


# def dos_draw(dos):
#     ax = plt.gca()
#     ax.plot([2,3],[4,2])


def plot_wann_bs(filepath='wannier90_band.dat', Ef=0.0):
    dirname = os.path.dirname(filepath)
    with open(os.path.join(dirname, 'wannier90_band.dat'), 'r') as f:
        data = f.readlines()
    blank_pos = [i for i, line in enumerate(data) if line.strip() == '']
    blank_pos.insert(0,-1)
    data_part = np.zeros(len(blank_pos)-1,dtype=object)

    for i in range(len(blank_pos)-1):
        data_part[i] = np.loadtxt(data[blank_pos[i]+1:blank_pos[i+1]])
        daxy = np.transpose(data_part[i])
        plt.plot(daxy[0],daxy[1]-Ef,'r--')
    plt.show('new.png')


