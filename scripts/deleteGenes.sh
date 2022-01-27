#!/usr/bin/env python3
import os
no_remove = set()
with open('/nfs1/BPP/LeBoldus_Lab/user_folders/mcmurtrs/cs_align/Busco/Tree/filteredGenes.txt') as f:       ##EDIT THIS LINE TO THE PATH TO YOUR FILE
     for line in f:
         no_remove.add(line.strip())

for f in os.listdir('.'):
    if f not in no_remove:
        print('unlink:' + f )
        os.unlink(f)
