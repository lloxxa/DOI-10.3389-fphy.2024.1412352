from importlib.resources import path
import pandas as pd
import io
from pathlib import Path
import os
import re
import json
from collections import defaultdict
import logging
import argparse

#input arguments
parser = argparse.ArgumentParser(description="A tool to convert rheocompass csv files to usefull datafiles and metadata")
parser.add_argument('input', help="Location of input .csv file or directory with multiple .csv files")
parser.add_argument("-o", "--output",
                    help="directory of output files")
parser.add_argument("-m", "--metadata", action="store_true",
                    help="export metadata")
parser.add_argument("-d", "--data", action="store_true",
                    help="export data")
parser.add_argument("-v", "--verbosity", action="count", default=0,
                    help="increase output verbosity")
args = parser.parse_args()

#logging handeling
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S', level=logging.ERROR)
if args.verbosity >= 2:
    logging.getLogger().setLevel(logging.NOTSET)
elif args.verbosity >= 1:
    logging.getLogger().setLevel(logging.WARNING)
else:
    logging.getLogger().setLevel(logging.ERROR)

def Main():
    if not args.data and not args.metadata:
        logging.critical("No conversion selected! Use -m of -d.")

    if args.output:
        if not os.path.exists(args.output):  os.mkdir(args.output)

    if os.path.isdir(args.input):
        logging.info("Directory found")
        directory = Path(args.input)

        for file in os.listdir(directory):
            filename = file
            if filename.endswith(".csv"):
                if args.data:
                    results(os.path.join(directory, filename), args.output)
                if args.metadata:   
                    metadata(os.path.join(directory, filename), args.output)
            else:
                continue 

    elif os.path.isfile(args.input):
        logging.info("File found")
        
        filename = Path(args.input)
        if args.data:
            results(filename, args.output)
        if args.metadata:
            metadata(filename, args.output)

    else:
        logging.critical("File or directory does not exist!")
        exit()

def results(input, output=""):
    if output == None: output = os.path.dirname(input)                          #If no output location has been given use the base path of the file
    filename = os.path.splitext(os.path.basename(input))[0]                     #extract only the name of the file
    with io.open(input,'r', encoding='utf-16') as f:                            #Open the file with a UTF-16 encoding
        print(f"Extracting results from {filename}.")
        try:
            file = f.read()                                                         #Read the whole file to "file"
        except:
            logging.critical(f"Cannot convert {filename}")
            return
        intervals = [i.end() for i in re.finditer("Interval data:", file)]      #Extract beginning and end indies for each interval and only use the end index
        for y,interval in enumerate(intervals):                                 #Go over each interval and convert to relavant data and format
            df = pd.read_csv(io.StringIO(file[interval:file.find('\n\n', interval)]), encoding='UTF-16', sep='\t', index_col=False) #Read interval into a dataframe
            for n,c in enumerate(df.columns):                                   #Enumerate over each column to combine the name and the unit. These are in 2 different rows.
                unit = str(df.iloc[1,n])                                        #get the unit form the second(1) row and n column
                if unit != "nan":                                               #Check if there is a unit
                    newCol = f"{c} {unit}"                                      #Combine name and unit
                    df = df.rename(columns={c:newCol})                          #Write new column name
            df = df.drop([0,1])                                                 #drop the first two rows, they never contain data
            df = df[~df['Point No.'].astype(str).str.contains("invalid", na=False)] #Remove all invalid points
            df = df.drop("Unnamed: 0", axis=1).reset_index(drop=True)           #drop the first column, it never contains any data
            if df.empty: continue                                               #if an interval is empty just continue without writing it to a file

            #If there is more then one interval write the results to a folder else write one result
            if len(intervals)>1: 
                OutDir = os.path.join(output, filename)
                if not os.path.exists(OutDir):  os.mkdir(OutDir)
                OutputName = os.path.join(OutDir, f"{filename}_Interval_{str(y+1)}.csv")
            else:
                OutputName = os.path.join(output, f"{filename}_Result.csv")

            df.to_csv(OutputName, index=False)                                  #write result to csv file

        if len(intervals)>1:
            print(f"DONE! The results can be found at {OutDir}")
        else:
            print(f"DONE! The result can be found at {output}")
    
def metadata(input, output=""):
    if output == None: output = os.path.dirname(input)                            #If no output location has been given use the base path of the file
    filename = os.path.splitext(os.path.basename(input))[0]                     #extract only the name of the file
    data = []
    with io.open(input,'r', encoding='utf-16') as f:
        try:
            file = f.read()                                                         #Read the whole file to "file"
        except:
            logging.critical(f"Cannot extract metadata from {filename}")
            return
        lines = file[:file.find("Interval and data points")]
        lines = lines.replace("=", "\t")
        data = [x for x in lines.split("\n") if x != ""]
        data = [x.split("\t") for x in data]

    nested_dict = lambda: defaultdict(nested_dict)
    result = nested_dict()
    temp = []
    skip = False
    level = ["","","","","",""]
    for n,items in enumerate(data):
        # Removing Description from data convert
        if items[0] == 'Description:' or skip:
            skip = True
            if data[n+1][0] != '':
                skip = False
            continue

            # Convert array
        length = len(items)
        for m in range(0,length-1):
            if n >= len(data)-1: 
                temp.append([level, items[length-2], items[length-1], True]) 
                continue
            if m >= len(data[n+1]): continue
            if data[n+1][m] == '' and items[m] != '':
                level[m] = items[m]
            elif data[n+1][m] != '' and items[m] == '':
                temp.append([level[:], items[length-2], items[length-1], True])
                for k in range(m,length-1):
                    level[k] = ""
                break 
            elif data[n+1][m] != '':
                temp.append([level[:], items[length-2], items[length-1] , False])
                level[m] = ""
    
    for n in temp:
        if n[0][0] == "":
            result[n[1]] = n[2]
        elif n[0][1] == "":
            result[n[0][0]][n[1]] = n[2]
        elif n[0][2] == "":
            result[n[0][0]][n[0][1]][n[1]] = n[2]
        elif n[0][3] == "":
            result[n[0][0]][n[0][1]][n[0][2]][n[1]] = n[2]
        elif n[0][4] == "":
            result[n[0][0]][n[0][1]][n[0][2]][n[0][3]][n[1]] = n[2]
        else:
            logging.warning("Not all metadata is included")

    OutputName = os.path.join(output, f"{filename}.json")
    with open(OutputName, 'w') as outfile:
        json.dump(result, outfile, indent=4, ensure_ascii=False)

Main()
    # print(f"Metadata of {filename} can be found at {output}")    
'''
if __name__ == "__main__":
    Main()
'''