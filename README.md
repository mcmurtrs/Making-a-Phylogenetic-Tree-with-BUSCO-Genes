# Making a Phylogenetic Tree with BUSCO genes

- All data being used for this tutorial can be found within the "data" folder within this directory.
- All custom scripts used within this tutorial are found in the "scripts" folder in this directory.

The data contained in this tutorial includes five seperate but closely related species of fungi. These fungi are often found within forest ecosystems. The names of these five fungi are:

- Coniferiporia sulphurascens (AP7)
- Coniferiporia weirii (PFC545)
- Phellinus lamaensis
- Phellinus noxious
- Porodaedalea pini

## Tutorial videos showing the steps
### Steps 1 and 2:
https://www.youtube.com/watch?v=gilA49YwSM4

### Steps 3 and 4:

https://www.youtube.com/watch?v=6KDvI74Ogzw

### Steps 5 and 6:
https://www.youtube.com/watch?v=ikEE6GGw0_0&t=43s

### Steps 7-11:
https://www.youtube.com/watch?v=pyMmFCCj1QA

### Final video tutorial
https://www.youtube.com/watch?v=eFb1MJUNGgg

A majority of the steps come from the following tutorials:

- https://github.com/chrishah/phylogenomics-intro
- https://bioinformaticsworkbook.org/phylogenetics/reconstructing-species-phylogenetic-tree-with-busco-genes-using-maximum-liklihood-method.html#gsc.tab=0

## Step 1: Setting up working directory, and centralizing all of our data
- Copy all the BUSCO "SAMPLEID_full_table.tsv" files to the working directory 
```
cd /nfs1/BPP/LeBoldus_Lab/user_folders/mcmurtrs/cs_align/Busco/Tree
cd pre_filter

```

## Step 2: Copy all "single_copy_busco_sequences" directories into Tree directory and rename to appropriate sample name

```
cp -r /nfs1/BPP/LeBoldus_Lab/user_folders/mcmurtrs/cs_align/De_novo/C_sulphurascens_Busco/run_basidiomycota_odb10/busco_sequences/single_copy_busco_sequences .
mv single_copy_busco_sequences C_sulphurascens 
```

## Step 3: Setup ingroup and outgroup text files.
- In our scenario we have 2 ingroups samples and 3 outgroup samples.
- Note a small amount of editing will need to be done to each file to delete the samples that are not in the in or out groups
- Use "ctrl + k" (on windows) to delete a line in nano editor
- In this simple example the samples in the "ingroup.txt" file are Coniferiporia sulphurascens species whereas the single sample in the "outgroup.txt" file is a Coniferiporia weirri sample.

### Ingroup

```
ls *.tsv > ingroup.txt
```

![image](https://user-images.githubusercontent.com/49656044/149902679-a76076e3-6b81-4d59-9265-9f5b170cf85b.png)

### Outgroup

```
ls *.tsv > outgroup.txt
```

![image](https://user-images.githubusercontent.com/49656044/149902729-d29508b9-f619-417c-b636-c8f06f7d78d4.png)


## Step 4: Look for all BUSCO genes present across all samples and filter them:
- We are filtering to help prevent false positive gene calls making their way into our dataset.  We are also filtering for quality. We will be using the python file called "evaluate.py" that can be found in the "scripts" folder of this repository.  If you would like to know more about this script please see the tutorial linked at the top of this page. 
- **** Parameters that we are filtering on are as follows: 
- No more than one sample missing for either the in- or the outgroup
- Average number of paralogs per sample <= 2 
- Median number of paralogs is <= 2 


```
python3 evaluate.py -i ingroup.txt -o outgroup.txt --max_mis_in 1 --max_mis_out 1 --max_avg 2 --max_med 2 --outfile summary.tsv -f *.tsv

```

![image](https://user-images.githubusercontent.com/49656044/149902531-95302af0-c9cf-4334-9a19-495060ea809c.png)


# Step 5: Make a list of all the BUSCO genes that passed the filtering process:
- The previous command outputs a file called "summary.tsv" that lists all of the Busco genes that passed. We will now use another python script to make a list of these genes. 

![image](https://user-images.githubusercontent.com/49656044/149904872-a13b6da5-4c3a-4a9a-8f83-f46f362469fc.png)

- We now want to use the python script file called "buscoList.py" to sort through the summary.tsv file and make a list of all the BUSCO genes that passed the filtering process.
- We open pythong 3, then run our buscoList.py script file, the python file iterates through our summary.tsv file line by line and prints passing gene results to a file called "filteredGenes.txt"
- The command looks like this:

```
python3 buscoList.py summary.tsv filteredGenes.txt
```

# Step 6: Delete all genes that didn't pass the filtering test:
- We need to get rid of all the genes that didn't pass our test.
- This next bash script will loop through each single copy BUSCO directory (i.e. SAMPLE1_Busco/run_basidiomycota_odb10/busco_sequences/single_copy_busco_sequences) and delete genes that didn't pass the test.
- The only caveots are that you need do this in every busco directory so if you have a lot you might want to automate it.
- Also make sure to edit line #4 to direct it towards the filteredGenes.txt file in your directory
- cd to each "single_copy_busco_sequences" directory 

```
cd U_maydis_genes
cp /home/bpp/mcmurtrs/my_dir/cs_align/Busco/Tree/evol_pre_filter/deleteGenes.sh .
./deleteGenes.sh    
```


- Don't forget to alter the path of line 4 if necessary to reflect the path to your filteredGenes.txt file
- The deleteGenes.sh script looks like this:
```
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
```


# Step 7: Check to ensure that there are equal amounts of genes within each gene file.
- To count the number of files in a directory use:
```
ls | wc -l
```
- If quantity of genes are not the same you can move the two folders to your desktop and cut and paste all the files from the directory with more files. 
- When asked if you would like to overwrite the files, select no.
- You should now have in the new directory files that are highlighted. These files should be the new files that need to be deleted.
- Paste the names of these files into a new file on the command line and use the following command to delete these files until you have two directories with equal amounts of files or genes.
- I know this was a lot of information and it is probably hard to follow. Watch video # **INSERT VIDEO NUMBER HERE** for a more detailed explaination.

```
#Copy the deleteThese.txt file that was made that included extra genes that aren't present in all samples that didn't get deleted for some reason:
cp /home/bpp/mcmurtrs/my_dir/cs_align/Busco/Tree/evol_pre_filter/deleteThese.txt .

#Command to nuke more of the genes so that all samples eventually have equal genes for further analysis.
xargs rm < deleteThese.txt

```

# Step 8: Delete the header line of each fasta file:
**There is a shortcut for doing this within multiple directories below the initial steps:**

```
sed -i '1d' *.faa
```
- Starting files look like this:

![image](https://user-images.githubusercontent.com/49656044/151456354-86e82dfd-a90c-40c6-9c9c-b738d1d29ac2.png)


- We want them all to look like this:

![image](https://user-images.githubusercontent.com/49656044/151456154-5796f228-f5e6-490d-a092-72befba8b902.png)


### Shortcut to do this within multiple directories at once:

```
#Testing
find . -maxdepth 1 -type d \( ! -name . \) -exec bash -c "cd '{}' && pwd" \;


# In action
find . -maxdepth 1 -type d \( ! -name . \) -exec bash -c "cd '{}' && sed -i '1d' *.faa" \;


```


# Step 9: Concatenate all the fasta files for each sample and change the ending of the file name to .fna
- For this example we will be doing this five times. Once for each group of fasta files that we have. 

```
cat *.faa* > combinedFasta_C_sulphurascens.fna
cat *.faa* > combinedFasta_C_weirri.fna
cat *.faa* > combinedFasta_F_mediterranea.fna
cat *.faa* > combinedFasta_P_lamaensis.fna
cat *.faa* > combinedFasta_P_pini.fna
cat *.faa* > combinedFasta_P_noxious.fna
cat *.faa* > combinedFasta_S_paradoxa.fna
cat *.faa* > combinedFasta_U_maydis.fna

cat *.faa* > combinedFasta_A_bisporus.fna
cat *.faa* > combinedFasta_A_subglabra.fna
cat *.faa* > combinedFasta_C_cinerea.fna
cat *.faa* > combinedFasta_C_neoformans.fna
cat *.faa* > combinedFasta_D_primogenitus.fna
cat *.faa* > combinedFasta_H_annosum.fna
cat *.faa* > combinedFasta_L_bicolor.fna
cat *.faa* > combinedFasta_P_indica.fna
cat *.faa* > combinedFasta_P_ostreatus.fna
cat *.faa* > combinedFasta_S_commune.fna
cat *.faa* > combinedFasta_S_niveocremeum.fna
cat *.faa* > combinedFasta_T_mesenterica.fna




```

# Step 10: Move all concatenated files with .fna ending to a new directory

```
cd /nfs1/BPP/LeBoldus_Lab/user_folders/mcmurtrs/cs_align/Busco/Tree/evol_pre_filter/combinedFastas
cp /nfs1/BPP/LeBoldus_Lab/user_folders/mcmurtrs/cs_align/Busco/Tree/evol_pre_filter/P_noxious_genes/combinedFasta_P_noxious.fna .

```


# Step 11: Concatenate all the fasta files ending in .fna to a new fasta file ending in .faa

```
cat *.fna* > combinedFastas.faa


```

# Step 12: Run multiple sequence alignment with mafft

```
# Running mafft (note this might need to be run on the cluster for large numbers of samples)
mafft combinedFastas.faa > combinedFastaFINAL.msa

# An example of what it looks like being run on the cluster at Oregon State University using current mafft version (mafft v. 7)
SGE_Batch -c 'mafft combinedFasta_C_weirri.faa > combinedFastaFINAL_v6.msa' -P 20 -r mafft_v6

# An example of what it looks like being run on the cluster at Oregon State University using an older mafft version (mafft v. 6)
SGE_Batch -c '/nfs1/BPP/LeBoldus_Lab/user_folders/mcmurtrs/bin/bin/mafft combinedFasta_C_weirri.faa > combinedFastaFINAL_v6.msa' -P 20 -r mafft_v6

# Output is in:
/nfs1/BPP/LeBoldus_Lab/user_folders/mcmurtrs/cs_align/Busco/Tree/evol_pre_filter/combinedFastas_copy
```

# Step 13: Open file in mesquite to visually inspect it
- blah blah blah

# Step 14: Export the file for RAxML using mesquite, move file back to cluster and run RAxML



![image](https://user-images.githubusercontent.com/49656044/150464632-c78b89fa-1a08-4abe-99bd-d09809aa3d9d.png)



# Step 15: Follow the steps at the tutorial listed below to make your tree with RAxML

- You can skip step 1 and go straight to step 2.
- Step 1 is used if you are starting with a vcf file and not a fasta file.

https://github.com/mcmurtrs/mcmurtrs.github.io/blob/main/ML%20Phylogenetic%20Tree/README.md
