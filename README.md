# Making a Phylogenetic Tree with BUSCO genes

A majority of the steps come from the following tutorials:

- https://github.com/chrishah/phylogenomics-intro
- https://bioinformaticsworkbook.org/phylogenetics/reconstructing-species-phylogenetic-tree-with-busco-genes-using-maximum-liklihood-method.html#gsc.tab=0

## Step 1: Setting up working directory
- Copy all the BUSCO "$SAMPLEID_full_table.tsv" files to the working directory directory 

```
/nfs1/BPP/LeBoldus_Lab/user_folders/mcmurtrs/cs_align/Busco/Tree
busco -i /nfs1/BPP/LeBoldus_Lab/user_folders/mcmurtrs/cs_align/De_novo_assembly/PWT131/contigs.fasta -l basidiomycota_odb10 -o PWT131_Busco -m geno
```

## Step 2: Setup ingroup and outgroup text files.
- In our scenario we have 98 ingroups samples and 11 outgroup samples.
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


## Step 3: Look for all BUSCO genes present across all samples and filter them:
- We are filtering to help prevent false positive gene calls making their way into our dataset.  We are also filtering for quality. We will be using the python file called "evaluate.py" that can be found in the "scripts" folder of this repository.  If you would like to know more about this script please see the tutorial linked at the top of this page. 
- **** Parameters that we are filtering on are as follows: 
- No more than one sample missing for either the in- or the outgroup
- Average number of paralogs per sample <= 2 
- Median number of paralogs is <= 2 


```
python3 evaluate.py -i ingroup.txt -o outgroup.txt --max_mis_in 1 --max_mis_out 1 --max_avg 2 --max_med 2 --outfile summary.tsv -f *.tsv

```

![image](https://user-images.githubusercontent.com/49656044/149902531-95302af0-c9cf-4334-9a19-495060ea809c.png)


# Step 4: Make a list of all the BUSCO genes that passed the filtering process:
- The previous command outputs a file called "summary.tsv" that lists all of the Busco genes that passed. We will now use another python script to make a list of these genes. 

![image](https://user-images.githubusercontent.com/49656044/149904872-a13b6da5-4c3a-4a9a-8f83-f46f362469fc.png)

- We now want to use the python script file called "buscoList.py" to sort through the summary.tsv file and make a list of all the BUSCO genes that passed the filtering process.
- We open pythong 3, then run our buscoList.py script file, the python file iterates through our summary.tsv file line by line and prints passing gene results to a file called "filteredGenes.txt"
- The command looks like this:

```
python3 buscoList.py summary.tsv filteredGenes.txt
```

# Step 5: Delete all genes that didn't pass the filtering test:
- We need to get rid of all the genes that didn't pass our test.
- This next bash script will loop through each single copy BUSCO directory (i.e. SAMPLE1_Busco/run_basidiomycota_odb10/busco_sequences/single_copy_busco_sequences) and delete genes that didn't pass the test.
- The only caveots are that you need do this in every busco directory so if you have a lot you might want to automate it.
- Also make sure to edit line #4 to direct it towards the filteredGenes.txt file in your directory
- cd to each "single_copy_busco_sequences" directory and run this script:

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

# Step 6: Add a prefix onto the genes that passed to attach them to each sample
- After you have finished deleted the genes we don't want add the prefix and cp all the files to a new directory called BUSCO_GENES

```
bash
#for file in *.faa; do mv "$file" "AP13_$file"; done;
for file in *.faa; do mv "$file" "AP7_$file"; done;
```


## Step 7: Adding a unique number to the beginning of each file name
``` n=1; for f in *; do mv "$f" "$((n++))_$f"; done ```



# Step 8:  Deleting the first line of each fasta file 
``` sed -i '1d' *.faa ```


 
# Step 9: Adding the unique name of the file to the first line of all files
- In order for clustalw to perform our multiple sample alignment, each fasta header needs to be unique.
- We can perform this within bash with sed.
 
 ``` sed -i '1F' *.faa ```

## Step 10: Adding '>' to the first line of each file
- This is again done for formatting purposes for clustalw. 
- Clustalw will ignore the first line that starts with a '>' symbol.
- The first line of our header should then look like the screenshot below.
- We have the carrot symbol, the unique id number, and our sample ID so we know what gene belongs to each sample. 

``` sed -i '1s/^/>/' * ```

![image](https://user-images.githubusercontent.com/49656044/150464632-c78b89fa-1a08-4abe-99bd-d09809aa3d9d.png)


## Step 11: Copy the freshly altered fasta files to the central directory called  
 
 ```
 cd /nfs1/BPP/LeBoldus_Lab/user_folders/mcmurtrs/cs_align/Busco/Tree/Fastas
 cp /nfs1/BPP/LeBoldus_Lab/user_folders/mcmurtrs/cs_align/Busco/Tree/C2_Busco/run_basidiomycota_odb10/busco_sequences/single_copy_busco_sequences/*.faa .

 ```
 
## Concat all fasta files into one fasta file
``` 



# Step 8: Concatenate all the fasta files together into one mega fasta file:
- An example of the combined fasta file can be found in the data folder. (INSERT DATA FOLDER AND COPY OF FASTA HERE!!) 

```
cd /nfs1/BPP/LeBoldus_Lab/user_folders/mcmurtrs/cs_align/Busco/Tree/ALL_BUSCOS
cat *.faa > combinedFasta.faa

```

# Step 8: Run alignment on combined fasta file with MAFFT

```
mafft combinedFasta.faa > finalFasta.faa

```

# Step 9: View the alignment with NCBI Multiple Sequence Alignment Viewer:

https://www.ncbi.nlm.nih.gov/projects/msaviewer/?appname=ncbi_msav&openuploaddialog

# Step 10: 
