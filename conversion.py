import pyAgrum 

bn=pyAgrum.loadBN('Brain_Tumor_original.xdsl')

pyAgrum.saveBN(bn,'Brain_Tumor_original.bif')