#!/bin/env python

import numpy
from math import log
from Bio.Alphabet import IUPAC
#import pdb

#caveats: if there are ambiguous residues present in the sequence, eg. in poly-A-tails, AAAANAAA, 
#this method will calculate artificially high complexity scores. It may be possible to get more
#accurate estimates, by ignoring these positions entirely.
#This prog does not merge low-complexity regions like seg/dust supposedly do

# original version by Estienne Swart
# from:  http://lists.open-bio.org/pipermail/biopython/2002-December/001134.html

class Complexity:
    """Class to calculate complexity given a sequence and window Ideally would like to inherit from Bio.Seq, TODO"""
    def __init__(self, seq, **kwds):
        """could make individual kwds more explicit here,
        Currently the class is initiated as follows:
        Complexity(seq = record, window = arguments["window"], alphabet = IUPAC.IUPACUnambiguousDNA())"""
        self.__dict__.update(kwds)
        self.sequence = seq.upper()
        self._calc_complexity_across_sequence()
        if self.mask:
            self.mask_sequence()

    def _factorial(self, n):
        '''A simple iterative factorial function. No range checking here yet'''
        if n > 0:
            factorial = 1
            for i in range(1, n +1): 
                factorial *= i
            return factorial
        else:
            return 1
    
    def _calc(self, seqportion):
        '''Calculate the complexity score here'''
        L = self.window
        L_factorial = self._factorial(L)
        multi_ni = 1
        for residue in self.alphabet.letters: 
            multi_ni *= self._factorial(seqportion.count(residue))
        return (float(1) / L) * (log(float(L_factorial) / multi_ni)) / log(len(self.alphabet.letters))

    def _calc_complexity_across_sequence(self):
        '''Calculate complexity of all sequence residues using a sliding window'''
        self.complexity_list = []
        for i in range(0, len(self.sequence) - self.window + 1):
            self.complexity_list.append(self._calc(self.sequence[i:i+self.window]))
        endbit = [self._calc(self.sequence[-self.window:])]
        for i in range(-1, -self.window + 1, -1):
            endbit.append(self._calc(self.sequence[i-self.window:i]))
        endbit.reverse()
        #need to calculate complexity scores for last few residues in the opposite direction then add them on
        self.complexity_list += endbit
        self.complexity_array = numpy.array(self.complexity_list)

    def mask_sequence(self):
        '''returns a low-complexity masked sequence masked residues are those 
        that fall below the threshold score form _calc.'''
        #pdb.set_trace()
        uc = numpy.array(list(self.sequence))
        lc = numpy.array(list(self.sequence.lower()))
        # get an array of boolean values indicating if we're < threshold
        bool_compare = self.complexity_array < self.threshold
        uc[bool_compare] = lc[bool_compare]
        self.masked = ''.join(uc)
        #pass

    def __repr__(self):
        #Unmask line below to get printout of complexity scores for each seq position
        #astr = str("""complexity (at each position) for a window of %(window)s:\n%(complexity_list)s 
        astr = str("""
        \nMasked at threshold %(threshold)s: %(masked)s\n""" % (self.__dict__))
        return astr