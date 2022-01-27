#!/local/cluster/bin/python3
import sys

#bring in user input file
wc_python_file = sys.argv[0]
wc_data_file = sys.argv[1]
wc_output_file = sys.argv[2]

#Write out header for our output file
output_file = open (wc_output_file, "w")
#output_file.write(f"This is \t the header  \n")



# rstrip the header line if you'd like to use or print it later
dF_handle = open(wc_data_file, "r")
rawHeaderLine = dF_handle.readline()
headerLine = rawHeaderLine.rstrip()
#print(f"First line of file is |{headerLine}|\n")


data_file_open = open(wc_data_file, "r")
for rawLine in dF_handle:
	line = rawLine.rstrip()         
        # If file is tab delimited get data items from the line
	lineparts_list = line.split("\t")
	
	#Identify items in BUSCO summary file
	BUSCO_ID = lineparts_list[0]
	N = lineparts_list[1]
	INGROUP = lineparts_list[2]
	OUTGROUP = lineparts_list[3]
	PARALOG = lineparts_list[4]
	COUNTS = lineparts_list[5]
	TEST = lineparts_list[6]



	#GENES THAT PASS THE TEST
	if TEST == "pass":
		output_file.write(f"{BUSCO_ID}.faa \n")

