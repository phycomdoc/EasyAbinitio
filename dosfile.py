import os
import os.path
import numpy as np


class Doscar(object):
    """
    Args:
        filename: filename of DOSCAR

    """
    def __init__(self, filename):
        self.nedos = None
        self.filename = filename
        self.e_fermi = 0
        self.tot_dos = None
        self.p_dos = None
        self.num_orbit = 9
        self.spd2int = {'s': 0, 'p1': 1, 'p2': 2, 'p3': 3,
                        'd1': 4, 'd2': 5, 'd3': 6, 'd4': 7, 'd5': 8}

        self.readfile()

    def readfile(self):
        """
        read DOSCAR file and extract dos information
        :return:
        """
        data = [line.split() for line in open(self.filename, 'r')]
        num_atom = int(data[0][0])
        emax, emin, nedos, e_fermi = data[5][:4]
        nedos = int(nedos)
        e_fermi = float(e_fermi)
        if len(data) == (nedos + 1) + 5:
            print("[info] the doscar doesnt have pdos")
            tot_dos = np.array(data[6:6 + nedos], dtype="float")
            self.tot_dos = tot_dos
        elif (num_atom + 1) * (nedos + 1) + 5 == len(data):
            print("[info] the doscar contains pdos")
            tot_dos = np.array(data[6:6 + nedos], dtype="float")
            p_dos = np.zeros((num_atom, nedos, self.num_orbit + 1))
            for i in range(num_atom):
                sliceobj = slice(6 + (i + 1) * (nedos + 1), 6 + (i + 1) * (nedos + 1) + nedos)
                p_dos[i] = np.array(data[sliceobj], dtype='float')
            self.p_dos = p_dos
            self.tot_dos = tot_dos

        self.e_fermi = e_fermi
        self.nedos = nedos

    def _spd_resolve(self, spd_tag):
        spd2int = {'s': 0, 'p1': 1, 'p2': 2, 'p3': 3,
                   'd1': 4, 'd2': 5, 'd3': 6, 'd4': 7, 'd5': 8, 'p': [1,2,3], 'd': [4,5,6,7,8]}

        try:
            spd = [spd2int[el] for el in spd_tag.split()]
        except KeyError:
            print("Error: the tag is not in the dict of spd")

        flat = lambda L: sum(map(flat, L), []) if isinstance(L, list) else [L]
        spd = flat(spd)
        return spd



    def pdos_selection(self, atom='1 ', spd='s p1 p2 p3 d1 d2 d3 d4 d5'):
        """
        single atom multiple orbital
        :param atom_spd:
        :return:
        """
        p_dos = self.p_dos
        spd = self._spd_resolve(spd)
        atom = [int(i) for i in atom.split()]
        sel_dos = np.zeros(self.nedos, dtype='float')
        for i in atom:
            for j in spd:
                sel_dos = sel_dos + p_dos[i-1, :, j+1]
                
        return sel_dos
